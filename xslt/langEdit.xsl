<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.loc.gov/mods/v3" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:mods="http://www.loc.gov/mods/v3"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:flvc="info:flvc/manifest/v1"
    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd"
    exclude-result-prefixes="xsl mods xs xsi"
    version="2.0">
    
    <xsl:output method="xml" version="1.0" byte-order-mark="no" encoding="UTF-8" indent="yes" />
    
    <xsl:template match='@* | node()'>
        <xsl:copy>
            <xsl:apply-templates select='@* | node()' />
        </xsl:copy>  
    </xsl:template>
    <xsl:template match="mods:language">
        <xsl:copy>
            <xsl:apply-templates select='@*|node()' />
            <xsl:if test="not(mods:languageTerm[@type='text']) and mods:languageTerm[@type='code']">
                <xsl:variable name="isoCode" select="mods:languageTerm[@type='code']" />
                <xsl:variable name="isoName" select="document('assets/isolang.xml')/languages/lang[@code=$isoCode]" />
                <languageTerm authority='iso639-2b' type='text'><xsl:value-of select="$isoName" /></languageTerm>
            </xsl:if>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>