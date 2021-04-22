CREATE DATABASE IF NOT EXISTS  `School` ;

USE `School`;



DROP TABLE IF EXISTS `assessments`;
CREATE TABLE `assessments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class` varchar(32) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `days_to_do` int DEFAULT NULL,
  `done` int DEFAULT NULL,
  PRIMARY KEY (`id`));



DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes`
(
    `task_id`            int       NOT NULL AUTO_INCREMENT,
    `Subject_Code`       varchar(64)    DEFAULT NULL,
    `Subject_Dscription` varchar(128)   DEFAULT NULL,
    `Group`              varchar(64)    DEFAULT NULL,
    `Activity`           varchar(64)    DEFAULT NULL,
    `Day`                varchar(8)     DEFAULT NULL,
    `Class_time`         time           DEFAULT NULL,
    `Campus`             varchar(16)    DEFAULT NULL,
    `Location`           varchar(32)    DEFAULT NULL,
    `staff`              varchar(64)    DEFAULT NULL,
    `Duration`           float          DEFAULT NULL,
    `Date`               date           DEFAULT NULL,
    `Class_Description`  varchar(64)    DEFAULT NULL,
    `Year`               int            DEFAULT NULL,
    `Sem`                int            DEFAULT NULL,
    `week`               int            DEFAULT NULL,
    `revision`           int            DEFAULT NULL,
    `last_date`          timestamp NULL DEFAULT NULL,
    `done`               int            DEFAULT NULL,
    PRIMARY KEY (`task_id`)
);

create definer = fonzzy@localhost view task_list as
select `a`.`id` AS `id`, `a`.`task_name` AS `task_name`, `a`.`task_date` AS `task_date`, `a`.`priority` AS `priority`
from (select concat('t_', `School`.`classes`.`task_id`)                                                           AS `id`,
             concat(left(`School`.`classes`.`Subject_Code`, 7), ' Week ', `School`.`classes`.`week`, ' ',
                    `School`.`classes`.`Group`, ' Rev ',
                    `School`.`classes`.`revision`)                                                                AS `task_name`,
             (`School`.`classes`.`Date` + interval (case
                                                        when (`School`.`classes`.`revision` = 0) then 0
                                                        when (`School`.`classes`.`revision` = 1) then 3
                                                        when (`School`.`classes`.`revision` = 2) then 7
                                                        else ((`School`.`classes`.`revision` - 2) * 14) end) day) AS `task_date`,
             (case when (`School`.`classes`.`revision` = 0) then 0.1 else 1 end)                                  AS `priority`
      from `School`.`classes`
      where ((`School`.`classes`.`Date` <= now()) and ((`School`.`classes`.`done` <> 1) or
                                                       ((`School`.`classes`.`done` = 1) and
                                                        (`School`.`classes`.`revision` = 0))) and
             ((`School`.`classes`.`Date` + interval (case
                                                         when (`School`.`classes`.`revision` = 0) then 0
                                                         when (`School`.`classes`.`revision` = 1) then 3
                                                         when (`School`.`classes`.`revision` = 2) then 7
                                                         else ((`School`.`classes`.`revision` - 2) * 14) end) day) <=
              now()))
      union all
      select concat('a', `School`.`assessments`.`id`)                                   AS `id`,
             concat(`School`.`assessments`.`class`, ' ', `School`.`assessments`.`name`) AS `task_name`,
             `School`.`assessments`.`due_date`                                          AS `task_date`,
             ((to_days(`School`.`assessments`.`due_date`) - to_days(now())) /
              (1 + `School`.`assessments`.`days_to_do`))                                AS `priority`
      from `School`.`assessments`
      where (((`School`.`assessments`.`due_date` + interval (-(1) * `School`.`assessments`.`days_to_do`) day) <=
              now()) and (`School`.`assessments`.`done` is null))) `a`
order by `a`.`priority`, `a`.`task_date`;