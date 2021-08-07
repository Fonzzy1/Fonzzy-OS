create table ref_pay_value
(
	id int auto_increment
		primary key,
	hours float null,
	pay_total float null,
	pay_take_home float null
);

create table ref_tax_amount
(
	val int null,
	lower_val int null,
	a float null,
	b float null
);

create table ref_week_conversion
(
	date date null,
	day varchar(3) null,
	week int null,
	`work cycle` int null,
	`rent cycle` int null,
	`utilities cycle` int null,
	`school week` int null,
	year int null,
	workday int default 0 null
);

create table tbl_expenses
(
	id int auto_increment
		primary key,
	name varchar(128) null,
	value int null,
	date date null,
	progress int default 0 null,
	cat varchar(32) null
);

create table tbl_expenses_cyclic
(
	id int auto_increment
		primary key,
	`desc` varchar(32) null,
	cat varchar(32) null,
	value varchar(32) null,
	cycle varchar(32) null
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

create table tbl_work
(
	id int auto_increment
		primary key,
	start_time timestamp not null,
	end_time timestamp null,
	comments text null
);

create  view vw_current_schedule as
	select `timetable`.`vw_schedule`.`concat('sr_',id)` AS `concat('sr_',id)`,
       `timetable`.`vw_schedule`.`project`          AS `project`,
       `timetable`.`vw_schedule`.`description`      AS `description`,
       `timetable`.`vw_schedule`.`date`             AS `date`,
       `timetable`.`vw_schedule`.`time`             AS `time`,
       `timetable`.`vw_schedule`.`location`         AS `location`,
       `timetable`.`vw_schedule`.`length`           AS `length`
from `timetable`.`vw_schedule`
where ((now() >= (cast(`timetable`.`vw_schedule`.`date` as datetime) +
                  interval ((`timetable`.`vw_schedule`.`time` / 10000) * 60) minute)) and (now() <=
                                                                                           (cast(`timetable`.`vw_schedule`.`date` as datetime) +
                                                                                            interval (
                                                                                                    ((`timetable`.`vw_schedule`.`time` +
                                                                                                      (`timetable`.`vw_schedule`.`length` * 10000)) /
                                                                                                     10000) *
                                                                                                    60) minute)));

create  view vw_cycle as
	select `a`.`name`        AS `cycle`,
       `a`.`number`      AS `number`,
       `b`.`date`        AS `date`,
       `b`.`work cycles` AS `work cycles`,
       `b`.`last cycle`  AS `first cycle`
from ((select 'week' AS `name`, min(`timetable`.`ref_week_conversion`.`week`) AS `number`
       from `timetable`.`ref_week_conversion`
       where ((`timetable`.`ref_week_conversion`.`date` >= cast(now() as date)) and
              (`timetable`.`ref_week_conversion`.`year` = year(cast(now() as date))))
       union all
       select 'rent' AS `rent`, min(`timetable`.`ref_week_conversion`.`rent cycle`) AS `number`
       from `timetable`.`ref_week_conversion`
       where (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date))
       union all
       select 'utilities' AS `utilities`, min(`timetable`.`ref_week_conversion`.`utilities cycle`) AS `number`
       from `timetable`.`ref_week_conversion`
       where (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date))
       union all
       select 'work' AS `utilities`, min(`timetable`.`ref_week_conversion`.`work cycle`) AS `number`
       from `timetable`.`ref_week_conversion`
       where (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date))) `a`
         join (select 'week'                                                AS `name`,
                      max(`timetable`.`ref_week_conversion`.`date`)         AS `date`,
                      (max(`timetable`.`ref_week_conversion`.`work cycle`) -
                       min(`timetable`.`ref_week_conversion`.`work cycle`)) AS `work cycles`,
                      min(`timetable`.`ref_week_conversion`.`work cycle`)   AS `last cycle`
               from `timetable`.`ref_week_conversion`
               where ((`timetable`.`ref_week_conversion`.`week` = (select min(`timetable`.`ref_week_conversion`.`week`)
                                                                   from `timetable`.`ref_week_conversion`
                                                                   where ((`timetable`.`ref_week_conversion`.`date` > cast(now() as date)) and
                                                                          (`timetable`.`ref_week_conversion`.`year` =
                                                                           year(cast(now() as date)))))) and
                      (`timetable`.`ref_week_conversion`.`year` = year(cast(now() as date))))
               union all
               select 'rent'                                                AS `rent`,
                      max(`timetable`.`ref_week_conversion`.`date`)         AS `max(date)`,
                      (max(`timetable`.`ref_week_conversion`.`work cycle`) -
                       min(`timetable`.`ref_week_conversion`.`work cycle`)) AS `work cycles`,
                      min(`timetable`.`ref_week_conversion`.`work cycle`)   AS `last cycle`
               from `timetable`.`ref_week_conversion`
               where (`timetable`.`ref_week_conversion`.`rent cycle` =
                      (select min(`timetable`.`ref_week_conversion`.`rent cycle`)
                       from `timetable`.`ref_week_conversion`
                       where (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date))))
               union all
               select 'utilities'                                           AS `utilities`,
                      max(`timetable`.`ref_week_conversion`.`date`)         AS `max(date)`,
                      (max(`timetable`.`ref_week_conversion`.`work cycle`) -
                       min(`timetable`.`ref_week_conversion`.`work cycle`)) AS `work cycles`,
                      min(`timetable`.`ref_week_conversion`.`work cycle`)   AS `last cycle`
               from `timetable`.`ref_week_conversion`
               where (`timetable`.`ref_week_conversion`.`utilities cycle` =
                      (select min(`timetable`.`ref_week_conversion`.`utilities cycle`)
                       from `timetable`.`ref_week_conversion`
                       where (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date))))
               union all
               select 'work'                                                AS `utilities`,
                      max(`timetable`.`ref_week_conversion`.`date`)         AS `max(date)`,
                      (max(`timetable`.`ref_week_conversion`.`work cycle`) -
                       min(`timetable`.`ref_week_conversion`.`work cycle`)) AS `work cycles`,
                      min(`timetable`.`ref_week_conversion`.`work cycle`)   AS `last cycle`
               from `timetable`.`ref_week_conversion`
               where (`timetable`.`ref_week_conversion`.`work cycle` =
                      (select min(`timetable`.`ref_week_conversion`.`work cycle`)
                       from `timetable`.`ref_week_conversion`
                       where (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date))))) `b`
              on ((`a`.`name` = `b`.`name`)));

create  view vw_cycle_expense as
	select `exp`.`name`                                       AS `name`,
       `exp`.`cat`                                        AS `cat`,
       ((`exp`.`value` - `exp`.`progress`) / greatest((`ref`.`work cycle` - (select `timetable`.`vw_cycle`.`number`
                                                                             from `timetable`.`vw_cycle`
                                                                             where (`timetable`.`vw_cycle`.`cycle` = 'work'))),
                                                      1)) AS `value`
from ((select `timetable`.`tbl_expenses`.`id`       AS `id`,
              `timetable`.`tbl_expenses`.`name`     AS `name`,
              `timetable`.`tbl_expenses`.`value`    AS `value`,
              `timetable`.`tbl_expenses`.`date`     AS `date`,
              `timetable`.`tbl_expenses`.`progress` AS `progress`,
              `timetable`.`tbl_expenses`.`cat`      AS `cat`
       from `timetable`.`tbl_expenses`
       union all
       select NULL                            AS `NULL`,
              `t`.`desc`                      AS `desc`,
              `t`.`value`                     AS `value`,
              `timetable`.`v`.`date`          AS `date`,
              ((((select `timetable`.`vw_cycle`.`number`
                  from `timetable`.`vw_cycle`
                  where (`timetable`.`vw_cycle`.`cycle` = 'work')) - `timetable`.`v`.`first cycle`) * `t`.`value`) /
               `timetable`.`v`.`work cycles`) AS `progress`,
              `t`.`cat`                       AS `cat`
       from (`timetable`.`tbl_expenses_cyclic` `t`
                join `timetable`.`vw_cycle` `v` on ((`t`.`cycle` = `timetable`.`v`.`cycle`)))) `exp`
         join `timetable`.`ref_week_conversion` `ref` on ((`ref`.`date` = `exp`.`date`)))
where (`exp`.`value` > `exp`.`progress`);

create  view vw_jobs as
	select `c`.`id`          AS `id`,
       `c`.`project`     AS `project`,
       `c`.`description` AS `description`,
       `c`.`length`      AS `length`,
       `c`.`due_date`    AS `due_date`,
       `c`.`due_time`    AS `due_time`
from (select concat('jd_', `timetable`.`tbl_jobs_due`.`id`) AS `id`,
             `timetable`.`tbl_jobs_due`.`project`           AS `project`,
             `timetable`.`tbl_jobs_due`.`description`       AS `description`,
             `timetable`.`tbl_jobs_due`.`length`            AS `length`,
             `timetable`.`tbl_jobs_due`.`due_date`          AS `due_date`,
             `timetable`.`tbl_jobs_due`.`due_time`          AS `due_time`
      from `timetable`.`tbl_jobs_due`
      where (`timetable`.`tbl_jobs_due`.`done` is null)
      union all
      select concat('jn_', `timetable`.`tbl_jobs_not_due`.`id`) AS `id`,
             `timetable`.`tbl_jobs_not_due`.`project`           AS `project`,
             `timetable`.`tbl_jobs_not_due`.`description`       AS `description`,
             `timetable`.`tbl_jobs_not_due`.`length`            AS `length`,
             cast((now() + interval 2 week) as date)            AS `date(date_add(now(), interval 2 week))`,
             '17:00:00'                                         AS `17:00:00`
      from `timetable`.`tbl_jobs_not_due`
      where (`timetable`.`tbl_jobs_not_due`.`done` is null)
      union all
      select concat('jr_', `timetable`.`tbl_jobs_recurring`.`id`)         AS `id`,
             `timetable`.`tbl_jobs_recurring`.`project`                   AS `project`,
             `timetable`.`tbl_jobs_recurring`.`description`               AS `description`,
             `timetable`.`tbl_jobs_recurring`.`length`                    AS `length`,
             (`timetable`.`tbl_jobs_recurring`.`last_date` +
              interval `timetable`.`tbl_jobs_recurring`.`redo_time` week) AS `date_add(last_date, interval redo_time week )`,
             '17:00:00'                                                   AS `17:00:00`
      from `timetable`.`tbl_jobs_recurring`
      where (`timetable`.`tbl_jobs_recurring`.`done` is null)) `c`
order by `c`.`due_date`, `c`.`due_time`, `c`.`id`;

create  view vw_pay_split as
	select `a`.`cat`                                                                                                AS `cat`,
       round(((sum(`a`.`value`) / (select `timetable`.`vw_work`.`total` from `timetable`.`vw_work`)) * 100), 0) AS `%`
from (select `timetable`.`vw_cycle_expense`.`name`  AS `name`,
             `timetable`.`vw_cycle_expense`.`cat`   AS `cat`,
             `timetable`.`vw_cycle_expense`.`value` AS `value`
      from `timetable`.`vw_cycle_expense`
      union all
      select 'Going Out' AS `Going Out`, 'Going Out' AS `Going Out`, `timetable`.`vw_work`.`Going Out` AS `Going Out`
      from `timetable`.`vw_work`
      union all
      select 'Savings' AS `Savings`, 'Savings' AS `Savings`, `timetable`.`vw_work`.`Savings` AS `Savings`
      from `timetable`.`vw_work`) `a`
group by `a`.`cat`;

create  view vw_payslip as
	select `timetable`.`ref_week_conversion`.`date`                                                                    AS `date`,
       `timetable`.`ref_week_conversion`.`day`                                                                     AS `day`,
       sum((timestampdiff(SECOND, `timetable`.`tbl_work`.`start_time`, `timetable`.`tbl_work`.`end_time`) /
            3600))                                                                                                 AS `hours`
from (`timetable`.`ref_week_conversion`
         left join `timetable`.`tbl_work`
                   on ((cast(`timetable`.`tbl_work`.`start_time` as date) = `timetable`.`ref_week_conversion`.`date`)))
where (`timetable`.`ref_week_conversion`.`work cycle` = (select `timetable`.`vw_cycle`.`number`
                                                         from `timetable`.`vw_cycle`
                                                         where (`timetable`.`vw_cycle`.`cycle` = 'work')))
group by `timetable`.`ref_week_conversion`.`day`, `timetable`.`ref_week_conversion`.`date`;

create  view vw_schedule as
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

create  view vw_week_calendar as
	select `c`.`project`                                                                                  AS `project`,
       `c`.`description`                                                                              AS `description`,
       `ref`.`day`                                                                                    AS `day`,
       cast((`c`.`date` + interval (`c`.`time` / 10000) hour) as time)                                AS `start`,
       cast(((`c`.`date` + interval (`c`.`time` / 10000) hour) + interval `c`.`length` hour) as time) AS `end`
from ((select concat('sr_', `s`.`id`) AS `concat('sr_',id)`,
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
         join `timetable`.`ref_week_conversion` `ref` on ((`c`.`date` = `ref`.`date`)))
where ((`ref`.`week` = (select `timetable`.`vw_cycle`.`number`
                        from `timetable`.`vw_cycle`
                        where (`timetable`.`vw_cycle`.`cycle` = 'week'))) and (`ref`.`year` = year(now())));

create  view vw_work as
	select least((select sum(`timetable`.`vw_cycle_expense`.`value`) from `timetable`.`vw_cycle_expense`),
             (select min(`timetable`.`ref_pay_value`.`pay_take_home`)
              from `timetable`.`ref_pay_value`
              where (`timetable`.`ref_pay_value`.`hours` >=
                     (select sum(`timetable`.`vw_payslip`.`hours`) from `timetable`.`vw_payslip`)))) AS `Expenses`,
       (select least(greatest(((select min(`timetable`.`ref_pay_value`.`pay_take_home`)
                                from `timetable`.`ref_pay_value`
                                where (`timetable`.`ref_pay_value`.`hours` >=
                                       (select sum(`timetable`.`vw_payslip`.`hours`) from `timetable`.`vw_payslip`))) -
                               (select sum(`timetable`.`vw_cycle_expense`.`value`)
                                from `timetable`.`vw_cycle_expense`)), 0), 250))                     AS `Going Out`,
       (select greatest((((select min(`timetable`.`ref_pay_value`.`pay_take_home`)
                           from `timetable`.`ref_pay_value`
                           where (`timetable`.`ref_pay_value`.`hours` >=
                                  (select sum(`timetable`.`vw_payslip`.`hours`) from `timetable`.`vw_payslip`))) -
                          (select sum(`timetable`.`vw_cycle_expense`.`value`) from `timetable`.`vw_cycle_expense`)) -
                         250), 0))                                                                   AS `Savings`,
       (select min(`timetable`.`ref_pay_value`.`pay_take_home`)
        from `timetable`.`ref_pay_value`
        where (`timetable`.`ref_pay_value`.`hours` >=
               (select sum(`timetable`.`vw_payslip`.`hours`) from `timetable`.`vw_payslip`)))        AS `total`,
       greatest((select count(0)
                 from (`timetable`.`ref_week_conversion`
                          join `timetable`.`vw_cycle`
                               on ((`timetable`.`vw_cycle`.`number` = `timetable`.`ref_week_conversion`.`work cycle`)))
                 where ((`timetable`.`vw_cycle`.`cycle` = 'work') and
                        (`timetable`.`ref_week_conversion`.`date` >= cast(now() as date)) and
                        (`timetable`.`ref_week_conversion`.`workday` = 1))), 1)                      AS `Days Left`;


