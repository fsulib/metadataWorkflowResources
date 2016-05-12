<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns="http://www.loc.gov/mods/v3"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:flvc="info:flvc/manifest/v1"
    xmlns:mods="http://www.loc.gov/mods/v3" 
    xmlns:dcterms="http://purl.org/dc/terms/"
    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd" exclude-result-prefixes="xs" version="1.0"> 
  
  <xsl:output encoding="UTF-8" method="xml"/>
  
  <!--    Template to change this:
        
        <location displayLabel="purl">
            <physicalLocation>Florida State University Libraries, Special Collections</physicalLocation>
            <url>http://purl.flvc.org/fcla/dt/2665306</url>
        </location>
    
        To this:
    
        <location displayLabel="purl">
            <url>http://purl.flvc.org/fcla/dt/1924932</url>
        </location>
    -->  
  
  <!-- Generic Identity Template -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  
  <xsl:template match="mods:location[@displayLabel='purl']">
    <location displayLabel="purl">
      <xsl:copy-of select="mods:url"/>  
    </location>
  </xsl:template>
</xsl:stylesheet>
