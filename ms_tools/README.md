# ms tools of Firmiana

This fold contains tools of processing mass spectrometry data.

Data source : import data to galaxy

file convert: convert files to open format

identification: tools of database search, quality control and quantifications.

===

Firmiana will scan the cloud folder or the ftp folder that hosts the MS files for analysis until MS file loading is finished. 

Then, Firmiana will automatically carry out protein identification with Mascot or X!Tandem and protein quantification. 

For protein identification, the false discovery rate (FDR) can be controlled on the peptide-spectrum match (PSM), peptide, and protein level. The default FDR is set at 1% on protein level. 

Label-free quantification is based on extracted ion chromatogram (XIC) and supports “match between runs”
