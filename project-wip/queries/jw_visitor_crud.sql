-- :name get_row_by_ip :one
select * from public."visitors" where visit_ip = :visit_ip

-- :name get_total_visit_count :one
select count(*) from public."visitors"  

-- :name get_all_visits :many
select * from public."visitors" 

-- :name insert_visit :insert
insert into public."visitors" (visit_time, visit_ip) values (:visit_time, :visit_ip)

-- :name delete_visit_by_time :affected
delete from public."visitors" where visit_time = :visit_time

-- :name delete_visit_by_ip :affected
delete from public."visitors" where visit_ip = :visit_ip


