-- upgrade --
ALTER TABLE `users` MODIFY COLUMN `password_hash` VARCHAR(128);
-- downgrade --
ALTER TABLE `users` MODIFY COLUMN `password_hash` VARCHAR(128) NOT NULL;
