CREATE TABLE "SalesTransaction" (
	"transaction_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL
);

INSERT INTO "SalesTransaction" VALUES (1, 1, 5);
INSERT INTO "SalesTransaction" VALUES (1, 2, 7);
INSERT INTO "SalesTransaction" VALUES (2, 3, 1);
INSERT INTO "SalesTransaction" VALUES (3, 2, 3);


---------------------------------------------------------------------------------------

CREATE TABLE "Product" (
	"product_id"	INTEGER NOT NULL,
	"product_name"	TEXT NOT NULL,
	"retail_price"	NUMERIC NOT NULL,
	"product_class_id"	INTEGER NOT NULL,
	PRIMARY KEY("product_id")
);


INSERT INTO "Product" VALUES (1, 'aa', 10, 1);
INSERT INTO "Product" VALUES (2, 'bb', 20, 1);
INSERT INTO "Product" VALUES (3, 'cc', 30, 2);


---------------------------------------------------------------------------------------


CREATE TABLE "ProductClass" (
	"product_class_id"	INTEGER NOT NULL,
	"product_class_name"	TEXT NOT NULL,
	PRIMARY KEY("product_class_id")
);

INSERT INTO "ProductClass" VALUES (1, 'Class A');
INSERT INTO "ProductClass" VALUES (2, 'Class B');
INSERT INTO "ProductClass" VALUES (3, 'Class C');


---------------------------------------------------------------------------------------

-- query
with T as (SELECT s.transaction_id,s.quantity,po.product_id,po.product_name,po.retail_price,p.product_class_name,s.quantity * po.retail_price as sales_value
from Product as po
inner join ProductClass as p on po.product_class_id = p.product_class_id
INNER join SalesTransaction as s on s.product_id = po.product_id)


SELECT * from (SELECT product_class_name,rank() OVER(PARTITION by product_class_name ORDER by sales_value desc) as ranking,product_name,sales_value from T) as F
where ranking < 3;