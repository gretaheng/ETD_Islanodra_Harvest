# ETD_Islanodra_Harvest

Before running any scripts, one needs to maker sure there are four folders in the same directory as the python scripts: idfiles, single_xml, merged_pre_upload, and final_output. 

- idfiles: Have two TXT files, one is id_bf.txt (hold downloaded ids), the other one is id_new_date.txt (hold ids to be downloaded)
- single_xml: Hold ETD XML records to be downloaded
- merged_pre_upload: Included one merged XML that needs some manual check
- final_output: Final output xml ready for ALMA import.


Two scripts are included in this folder. 


- HarvestFromIslandora.py: This file check for new ETD records in Islandora, download new records, and create one merged XML record in the merged_pre_upload folder. To run this script, run the following line in the command "python (path of this script) last_page_number_of_ETD_collection_in_Islandora full_path_of_the_folder_that_holds_the_four_folders_above date" 


- ChangeURI.py: After manual validating the merged XML file, update the Identifier[@type=url] element for each record, which will be the access method for users. To run this script, run the following line in the command "python (path of this script) full_path_of_the_merged_xml_in_the_merged_pre_upload_folder full_path_of_the_new_XML_(should be in the final_output folder)"
