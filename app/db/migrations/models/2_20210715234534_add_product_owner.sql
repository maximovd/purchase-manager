-- upgrade --
ALTER TABLE `products` ADD `owner_id` INT NOT NULL;
ALTER TABLE `products` ADD CONSTRAINT `fk_products_users_47f9f68f` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
-- downgrade --
ALTER TABLE `products` DROP FOREIGN KEY `fk_products_users_47f9f68f`;
ALTER TABLE `products` DROP COLUMN `owner_id`;
