# SourceCode / ms tools in Galaxy

ms tools directory contains tools of processing mass spectrometry data in Galaxy.

- Data source : import data to galaxy
  - aliyun_delete.py: delete files in aliyun OSS
  - aliyun_download.py: Download files from aliyun OSS
  - cycle_check_file_cloud.py: copy files from oss to galaxy
  - cycle_check_file_local.py: copy files from nas/ftp to galaxy
  - findError.py:
  - rename.py: import files to galaxy and start workflow
  - truncateExp.py: truncate the results of specific experiment
- file convert: convert files to open format
  - mascot2XML.py: convert mascot result to xml format
  - mzXML2Search.py:convert mzXML format to mgf format
  - mzXML_parser.py: mzXML format parser
  - noscan_wiff2mzXML.py: convert abi wiff files to mzXML
  - raw2mzXML.py: convert Thermo raw files to mzXML
  - wiff2mzXML.py: convert abi wiff fils and scan files to mzXML
- identification: tools of database search, quality control and quantifications.
  - QC_mascotdat_parser.py
  - cal_area.py: module of label free quantification
  - decoy.pl:External library from mascot to create decoy database.
  - get_search_param.py: get parameters of experiment
  - interProphet.py: integrate interProphet into Galaxy
  - mascot.py: search files using mascot
  - mascotdat_parser.py: parse the result from mascot
  - mayu.py: External tools from TPP to calculate FDR.
  - msparser.py: External mascot result parser library from mascot.
  - peptideProphet.py:External tools from TPP to calculate FDR.
  - proteinProphet.xml:External tools from TPP to calculate FDR.
  - xtandem.py: search files using X!Tandem
- models
  - firmiana_sendmail.py: Send emails when workflows is already done
  - gardener_control.py: Custom functional script used for connecting database of Firmiana.
  - msparser.py:External mascot result parser library from mascot.

---

Firmiana will scan the cloud folder or the ftp folder that hosts the MS files for analysis until MS file loading is finished. 

Then, Firmiana will automatically carry out protein identification with Mascot or X!Tandem and protein quantification. 

For protein identification, the false discovery rate (FDR) can be controlled on the peptide-spectrum match (PSM), peptide, and protein level. The default FDR is set at 1% on protein level. 

Label-free quantification is based on extracted ion chromatogram (XIC) and supports “match between runs”
