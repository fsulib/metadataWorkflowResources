<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	exclude-result-prefixes="xs"
	version="2.0">
	
	<!-- This stylesheet removes the identifer elements with @type=file. -->
	<xsl:output method="xml" version="1.0" byte-order-mark="no" encoding="UTF-8" indent="yes" />
		<xsl:template match="node()|@*">
			<xsl:copy>
				<xsl:apply-templates select="node()|@*"/>
			</xsl:copy>
		</xsl:template>
	<xsl:template match="//identifier[@type='file']"/>
</xsl:stylesheet>