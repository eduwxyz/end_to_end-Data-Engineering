{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, lpep_pickup_datetime) as rn
  from {{ source('raw_data','trips_green') }}
  where vendorid is not null )



select 
    {{ dbt_utils.surrogate_key(['vendorid', 'lpep_pickup_datetime', 'rn']) }} as id,
    lpep_pickup_datetime as pickup_datetime,
    lpep_dropoff_datetime as dropoff_datetime,
from tripdata




