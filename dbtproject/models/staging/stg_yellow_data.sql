{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, tpep_pickup_datetime) as rn
  from {{ source('raw_data','trips_yellow') }}
  where vendorid is not null )



select 
    {{ dbt_utils.surrogate_key(['vendorid', 'tpep_pickup_datetime', 'rn']) }} as id,
    tpep_pickup_datetime as pickup_datetime,
    tpep_dropoff_datetime as dropoff_datetime,
from tripdata




