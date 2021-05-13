create table ref_week_conversion
(
	date date null,
	day varchar(3) null,
	week int null,
	cycle int null,
	term int null,
	semester int null,
	year int null
);

create table tbl_jobs_due
(
	id int auto_increment
		primary key,
	project varchar(32) null,
	description varchar(64) null,
	length float null,
	due_date date null,
	due_time time null,
	done binary(1) null
);

create table tbl_jobs_not_due
(
	id int auto_increment
		primary key,
	project varchar(32) null,
	description varchar(64) null,
	length float null,
	done binary(1) null
);

create table tbl_jobs_recurring
(
	id int auto_increment
		primary key,
	project varchar(32) null,
	description varchar(64) null,
	length float null,
	redo_time int null,
	last_date date null,
	done binary(1) null
);

create table tbl_schedule_one_off
(
	id int auto_increment
		primary key,
	project varchar(32) null,
	description varchar(64) null,
	date date null,
	time time null,
	length float null,
	location varchar(32) null
);

create table tbl_schedule_recurring
(
	id int auto_increment
		primary key,
	project varchar(32) null,
	description varchar(64) null,
	day varchar(3) null,
	time time null,
	length float null,
	location varchar(32) null,
	done binary(1) null
);

create definer = fonzzy@localhost view vw_jobs as
	select `c`.`concat('jd_',id)` AS `concat('jd_',id)`,
       `c`.`project`          AS `project`,
       `c`.`description`      AS `description`,
       `c`.`length`           AS `length`,
       `c`.`due_date`         AS `due_date`,
       `c`.`due_time`         AS `due_time`
from (select concat('jd_', `timetable`.`tbl_jobs_due`.`id`) AS `concat('jd_',id)`,
             `timetable`.`tbl_jobs_due`.`project`           AS `project`,
             `timetable`.`tbl_jobs_due`.`description`       AS `description`,
             `timetable`.`tbl_jobs_due`.`length`            AS `length`,
             `timetable`.`tbl_jobs_due`.`due_date`          AS `due_date`,
             `timetable`.`tbl_jobs_due`.`due_time`          AS `due_time`
      from `timetable`.`tbl_jobs_due`
      where (`timetable`.`tbl_jobs_due`.`done` is null)
      union all
      select concat('jn_', `timetable`.`tbl_jobs_not_due`.`id`) AS `concat('jn_',id)`,
             `timetable`.`tbl_jobs_not_due`.`project`           AS `project`,
             `timetable`.`tbl_jobs_not_due`.`description`       AS `description`,
             `timetable`.`tbl_jobs_not_due`.`length`            AS `length`,
             cast((now() + interval 2 week) as date)            AS `date(date_add(now(), interval 2 week))`,
             '17:00:00'                                         AS `17:00:00`
      from `timetable`.`tbl_jobs_not_due`
      where (`timetable`.`tbl_jobs_not_due`.`done` is null)
      union all
      select concat('jr_', `timetable`.`tbl_jobs_recurring`.`id`)         AS `concat('jr_',id)`,
             `timetable`.`tbl_jobs_recurring`.`project`                   AS `project`,
             `timetable`.`tbl_jobs_recurring`.`description`               AS `description`,
             `timetable`.`tbl_jobs_recurring`.`length`                    AS `length`,
             (`timetable`.`tbl_jobs_recurring`.`last_date` +
              interval `timetable`.`tbl_jobs_recurring`.`redo_time` week) AS `date_add(last_date, interval redo_time week )`,
             '17:00:00'                                                   AS `17:00:00`
      from `timetable`.`tbl_jobs_recurring`
      where (`timetable`.`tbl_jobs_recurring`.`done` is null)) `c`
order by `c`.`due_date`, `c`.`due_time`;

create definer = fonzzy@localhost view vw_schedule as
	select `c`.`concat('sr_',id)` AS `concat('sr_',id)`,
       `c`.`project`          AS `project`,
       `c`.`description`      AS `description`,
       `c`.`date`             AS `date`,
       `c`.`time`             AS `time`,
       `c`.`location`         AS `location`,
       `c`.`length`           AS `length`
from (select concat('sr_', `s`.`id`) AS `concat('sr_',id)`,
             `s`.`project`           AS `project`,
             `s`.`description`       AS `description`,
             `r`.`date`              AS `date`,
             `s`.`time`              AS `time`,
             `s`.`location`          AS `location`,
             `s`.`length`            AS `length`
      from (`timetable`.`tbl_schedule_recurring` `s`
               join `timetable`.`ref_week_conversion` `r` on (((`s`.`day` = `r`.`day`) and (`s`.`done` is null))))
      union all
      select concat('sof_', `timetable`.`tbl_schedule_one_off`.`id`) AS `concat('sof_',id)`,
             `timetable`.`tbl_schedule_one_off`.`project`            AS `project`,
             `timetable`.`tbl_schedule_one_off`.`description`        AS `description`,
             `timetable`.`tbl_schedule_one_off`.`date`               AS `date`,
             `timetable`.`tbl_schedule_one_off`.`time`               AS `time`,
             `timetable`.`tbl_schedule_one_off`.`location`           AS `location`,
             `timetable`.`tbl_schedule_one_off`.`length`             AS `length`
      from `timetable`.`tbl_schedule_one_off`) `c`
where ((now() < ((cast(`c`.`date` as datetime) + cast(`c`.`time` as time)) + interval `c`.`length` hour)) and
       (`c`.`date` < (now() + interval 1 week)))
order by `c`.`date`, `c`.`time`;

