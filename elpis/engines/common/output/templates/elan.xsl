<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv2.7.xsd" version="2.0" xml:lang="en">
<xsl:output method="xml" doctype-public="-//W3C//DTD HTML 5 Transitional//EN" encoding="utf-8" indent="yes"/>

<xsl:param name="author" select="'elpis-espnet'"/>
<xsl:param name="version" select="'2.8'"/>
<xsl:param name="participant" select="'unknown'"/>
<xsl:param name="audio_path"/>
<xsl:param name="relative_audio_path"/>
<xsl:param name="tier_id" select="'default'"/>
<xsl:param name="source_language_code" select="'unknown'"/>

<xsl:template match="data">
    <ANNOTATION_DOCUMENT>
        <xsl:attribute name="xsi:noNamespaceSchemaLocation">
            <xsl:text>http://www.mpi.nl/tools/elan/EAFv2.7.xsd</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="DATE">
            <xsl:value-of select="current-dateTime()"/>
        </xsl:attribute>
        <xsl:attribute name="AUTHOR">
            <xsl:value-of select="$author"/>
        </xsl:attribute>
        <xsl:attribute name="VERSION">
            <xsl:value-of select="$version"/>
        </xsl:attribute>
        <xsl:call-template name="header"/>
        <xsl:variable name="time_slots">
            <xsl:call-template name="create_time_slots"/>
        </xsl:variable>
        <xsl:call-template name="TIME_ORDER">
            <xsl:with-param name="time_slots" select="$time_slots"/>
        </xsl:call-template>
        <xsl:call-template name="TIER">
            <xsl:with-param name="time_slots" select="$time_slots"/>
        </xsl:call-template>
        <xsl:call-template name="LINGUISTIC_TYPE"/>
    </ANNOTATION_DOCUMENT>
</xsl:template>

<xsl:template name="header">
    <HEADER>
        <xsl:attribute name="MEDIA_FILE">
            <xsl:text></xsl:text>
        </xsl:attribute>
        <xsl:attribute name="TIME_UNITS">
            <xsl:text>milliseconds</xsl:text>
        </xsl:attribute>
        <xsl:apply-templates select="audio_path"/>
    </HEADER>
</xsl:template>

<xsl:template match="audio_path">
    <MEDIA_DESCRIPTOR>
        <xsl:attribute name="MEDIA_URL">
            <xsl:value-of select="$audio_path"/>
        </xsl:attribute>
        <xsl:attribute name="MIME_TYPE">
            <xsl:text>audio/x-wav</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="RELATIVE_MEDIA_URL">
            <xsl:value-of select="$relative_audio_path"/>
        </xsl:attribute>
        <xsl:attribute name="TIME_ORIGIN">
            <xsl:text>0</xsl:text>
        </xsl:attribute>
    </MEDIA_DESCRIPTOR>
</xsl:template>

<xsl:template name="TIME_ORDER">
    <xsl:param name="time_slots"/>
    <TIME_ORDER>
        <xsl:copy-of select="$time_slots"/>
    </TIME_ORDER>
</xsl:template>

<xsl:template name="TIME_SLOT">
    <xsl:param name="position"/>
    <TIME_SLOT>
        <xsl:attribute name="TIME_SLOT_ID">
            <xsl:text>ts</xsl:text>
            <xsl:value-of select="$position"/>
        </xsl:attribute>
        <xsl:attribute name="TIME_VALUE">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </TIME_SLOT>
</xsl:template>

<xsl:template name="create_time_slots">
    <xsl:variable name="time_slots">
        <xsl:for-each select="segments/segment">
            <time_slot><xsl:value-of select="format-number(start*1000, '0000000000')"/></time_slot>
            <time_slot><xsl:value-of select="format-number(end*1000, '0000000000')"/></time_slot>
        </xsl:for-each>
    </xsl:variable>
    <!-- Removal of duplicated time values for cleaner XML. -->
    <xsl:variable name="time_slots">
        <xsl:for-each-group select="$time_slots/time_slot" group-by=".">
            <xsl:call-template name="TIME_SLOT">
                <xsl:with-param name="position" select="position()"/>
            </xsl:call-template>
        </xsl:for-each-group>
    </xsl:variable>
    <xsl:copy-of select="$time_slots"/>
</xsl:template>

<xsl:template name="TIER">
    <xsl:param name="time_slots"/>
    <TIER>
        <xsl:attribute name="TIER_ID">
            <xsl:value-of select="$tier_id"/>
        </xsl:attribute>
        <xsl:attribute name="LINGUISTIC_TYPE_REF">
            <xsl:text>default-lt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="PARTICIPANT">
            <xsl:value-of select="$participant"/>
        </xsl:attribute>
        <xsl:attribute name="DEFAULT_LOCALE">
            <xsl:value-of select="$source_language_code"/>
        </xsl:attribute>
        <xsl:apply-templates select="segments/segment">
            <xsl:with-param name="time_slots" select="$time_slots"/>
        </xsl:apply-templates>
    </TIER>
</xsl:template>

<xsl:template match="segment">
    <xsl:param name="time_slots"/>
    <ANNOTATION>
        <ALIGNABLE_ANNOTATION>
            <xsl:attribute name="ANNOTATION_ID">
                <xsl:value-of select="utterance_id"/>
            </xsl:attribute>
            <xsl:attribute name="TIME_SLOT_REF1">
                <xsl:variable name="time_value" select="format-number((start*1000), '0000000000')"/>
                <xsl:value-of select="$time_slots/TIME_SLOT[@TIME_VALUE=$time_value]/@TIME_SLOT_ID"/>
            </xsl:attribute>
            <xsl:attribute name="TIME_SLOT_REF2">
                <xsl:variable name="time_value" select="format-number((end*1000), '0000000000')"/>
                <xsl:value-of select="$time_slots/TIME_SLOT[@TIME_VALUE=$time_value]/@TIME_SLOT_ID"/>
            </xsl:attribute>
            <ANNOTATION_VALUE>
                <xsl:value-of select="replace(text, '<eos>', '')"/>
            </ANNOTATION_VALUE>
        </ALIGNABLE_ANNOTATION>
    </ANNOTATION>
</xsl:template>

<xsl:template name="LINGUISTIC_TYPE">
    <LINGUISTIC_TYPE>
        <xsl:attribute name="LINGUISTIC_TYPE_ID">
            <xsl:text>default-lt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="TIME_ALIGNABLE">
            <xsl:text>true</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="GRAPHIC_REFERENCES">
            <xsl:text>false</xsl:text>
        </xsl:attribute>
    </LINGUISTIC_TYPE>
    <LINGUISTIC_TYPE>
        <xsl:attribute name="LINGUISTIC_TYPE_ID">
            <xsl:text>meta</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="TIME_ALIGNABLE">
            <xsl:text>false</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="GRAPHIC_REFERENCES">
            <xsl:text>false</xsl:text>
        </xsl:attribute>
    </LINGUISTIC_TYPE>
</xsl:template>

</xsl:stylesheet>
