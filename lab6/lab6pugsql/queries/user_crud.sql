-- :name get_one_user :one
select * from public."User" where email = :email

-- :name get_all_users :many
select * from public."User" 

-- :name insert_user :insert
insert into public."User" (email, name) values (:email, :name)

-- :name delete_one_user :affected
delete from public."User" where email = :email

-- :name update_one_user :affected
update public."User" set name = :name where email = :email
