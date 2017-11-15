<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mods="http://www.loc.gov/mods/v3" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	 xmlns:flvc="info:flvc/manifest/v1"
    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output method="xml" name="xml"/>
    
    <xsl:template match="/">
        <xsl:for-each select="//mods:mods">
            <xsl:variable name="filename" select="concat('MODS/',translate(translate(mods:identifier[@type='fedora'],' &#x9;&#xa;&#xd;.',''),' &#x9;&#xa;&#xd;.',''),'.xml')" />
            <xsl:value-of select="$filename" />
            <xsl:result-document href="{$filename}" format="xml">
                <xsl:copy-of select="." />
            </xsl:result-document>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
