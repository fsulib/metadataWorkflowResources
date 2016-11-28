import logging
import requests
from lxml import etree
from bs4 import BeautifulSoup


nameSpace_default = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 
                     'dc': 'http://purl.org/dc/elements/1.1/', 
                     'mods': 'http://www.loc.gov/mods/v3', 
                     'dcterms': 'http://purl.org/dc/terms'}

class lc_subject:
    subject_parts = {}
    
    # TGM simple
    def tgm_simple(subject_LOC_reply): 
        subject_html = subject_LOC_reply.text
        subject_uri = subject_LOC_reply.url[0:-5]
        subject_soup = BeautifulSoup(subject_html, 'lxml')
        for authority_div in subject_soup.find_all('div', about=subject_uri):
            
            # look for RDFa in anchor elements
            if authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel") is not None:
                subject_heading = authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel").text
            
            # look for RDFa in span elements
            elif authority_div.find('a', property="madsrdf:authoritativeLabel skos:prefLabel") is not None:
                subject_heading = authority_div.find('a', property="madsrdf:authoritativeLabel skos:prefLabel").text
            # check for "Use Instead" url

            elif authority_div.find('span', property="madsrdf:variantLabel skosxl:literalForm"):
                use_instead = authority_div.find('h3', text="Use Instead")        
                variant_URI = use_instead.find_next('a').text                          
                # try again with "Use Instead" url
                subject_heading = lc_subject.tgm_simple(requests.get(variant_URI, timeout=5))[1]
                subject_uri = variant_URI             
        return subject_uri, subject_heading
            
    # LCSH simple    
    def lcsh_simple(subject_LOC_reply):
        subject_html = subject_LOC_reply.text
        subject_uri = subject_LOC_reply.url[0:-5]
        subject_soup = BeautifulSoup(subject_html, 'lxml')
        for authority_div in subject_soup.find_all('div', about=subject_uri):

            # look for RDFa in anchor elements
            if authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel") is not None:
                subject_heading = authority_div.find('span', property="madsrdf:authoritativeLabel skos:prefLabel").text
            
            # look for RDFa in span elements
            elif authority_div.find('a', property="madsrdf:authoritativeLabel skos:prefLabel") is not None:
                subject_heading = authority_div.find('a', property="madsrdf:authoritativeLabel skos:prefLabel").text
                
            # check for "Use Instead" url
            elif authority_div.find('span', property="madsrdf:variantLabel skosxl:literalForm"):
                use_instead = authority_div.find('h3', text="Use Instead")        
                variant_URI = use_instead.find_next('a').text                          
                # try again with "Use Instead" url
                subject_heading = lc_subject.lcsh_simple(requests.get(variant_URI, timeout=5))[1]
                subject_uri = variant_URI                
            
        return subject_uri, subject_heading       
    
    # LCSH complex
    def lcsh_complex(subject_LOC_reply):
        subject_parts = {}
        subject_parts['URI'] = subject_LOC_reply.url[0:-5]
        
        # indiviual subject elements are return as a list of dicts:
        # heading : term
        subject_parts['parts'] = []
        subject_soup = BeautifulSoup(subject_LOC_reply.text, 'lxml')
        for componentList in subject_soup.find_all("ul", rel="madsrdf:componentList"):
            for heading in componentList.find_all('div'):
                if 'madsrdf:Authority' in heading.get('typeof'):
                    subject_parts['parts'].append( { heading['typeof'].split(' ')[2].split(':')[1].lower() : 
                    heading.text.strip() } )
        return subject_parts


def write_record_subjects(record, subjects, PID):
    with open('improvedMODS/' + PID.replace(':','_') + '.xml', 'w') as MODS_out:
        
        # loop over incoming subjects
        for appending_subject in subjects:
            
            # build tgm subjects
            if 'tgm' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='lctgm', 
                                        authorityURI=appending_subject['tgm'][0][0:45],
                                        valueURI=appending_subject['tgm'][0])
                topic = etree.SubElement(subject, '{%s}topic' % nameSpace_default['mods'])
                topic.text = appending_subject['tgm'][1]
            
            # build lcsh simple
            elif 'lcsh_simple' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='lcsh', 
                                        authorityURI=appending_subject['lcsh_simple'][0][0:38],
                                        valueURI=appending_subject['lcsh_simple'][0])
                topic = etree.SubElement(subject, '{%s}topic' % nameSpace_default['mods'])
                topic.text = appending_subject['lcsh_simple'][1]
            
            
            # build lcsh complex
            elif 'lcsh_complex' in appending_subject.keys():
                subject = etree.Element('{%s}subject' % nameSpace_default['mods'],
                                        authority='lcsh',
                                        authorityURI=appending_subject['lcsh_complex']['URI'][0:38],
                                        valueURI=appending_subject['lcsh_complex']['URI'])
                for part in appending_subject['lcsh_complex']['parts']:
#                    print(part)
                
                    for type, term in part.items():
                        child = etree.SubElement(subject, '{%s}%s' % ( nameSpace_default['mods'], type ),)
                        child.text = term
                
            record.append(subject)

        # write new records    
        MODS_out.write(etree.tostring(record, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode('utf-8'))
        
class uri_lookup:

    #TGM
    def tgm(keyword, record_PID):
    
        global LOC_try_index
        global error_log
        tgm_lookup = requests.get('http://id.loc.gov/vocabulary/graphicMaterials/label/{0}'.format(keyword.replace(' ','%20')),
                                   timeout=5)
        # request successful                           
        if tgm_lookup.status_code == 200:
            LOC_try_index = 0
            return lc_subject.tgm_simple(tgm_lookup)
        # 404    
        elif tgm_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'tgm:' + keyword))
            error_log = True
            return None
        # 503 (probably wait... but haven't caught one of these yet)    
        elif tgm_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'tgm:' + keyword))
            error_log = True
            return None
        # anything else
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'tgm:' + keyword))
            error_log = True
            return None
    
    #LCSH simple
    def lcsh(keyword, record_PID):

        global LOC_try_index
        global error_log
        lcsh_lookup = requests.get('http://id.loc.gov/authorities/subjects/label/{0}'.format(keyword.replace(' ','%20')),
                                    timeout=5)
        # request successful
        if lcsh_lookup.status_code == 200:
            LOC_try_index = 0
            return lc_subject.lcsh_simple(lcsh_lookup)
        # 404
        elif lcsh_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        # 503 (probably wait... but haven't caught one of these yet)
        elif lcsh_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        # anything else
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
            
    #LCSH complex
    def lcsh_complex(keyword, record_PID):

        global LOC_try_index
        global error_log
        lcsh_lookup = requests.get('http://id.loc.gov/authorities/subjects/label/{0}'.format(keyword.replace(' ','%20')),
                                    timeout=5)
        # request successful
        if lcsh_lookup.status_code == 200:
            LOC_try_index = 0
            return lc_subject.lcsh_complex(lcsh_lookup)
        # 404
        elif lcsh_lookup.status_code == 404:
            logging.warning('404 - resource not found ; [{0}]--{1}'.format(record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        # 503 (probably wait... but haven't caught one of these yet)
        elif lcsh_lookup.status_code == 503:
            logging.info('503 - {0} ; [{1}]--{2}'.format(tgm_lookup.headers, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None
        # anything else
        else:
            logging.warning('Other status code - {0} ; [{1}]--{2}'.format(tgm_lookup.status_code, record_PID, 'lcsh:' + keyword))
            error_log = True
            return None