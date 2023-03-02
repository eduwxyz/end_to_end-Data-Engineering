variable "project" {}

variable "credentials_file" {}

variable "region" {
  default = "US"
}

variable "zone" {
  default = "US"
}


variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}



variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "raw_data"
}


locals {
  data_lake_bucket = "dtc_data_lake"
}
