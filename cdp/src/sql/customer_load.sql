/*
	Customer Profile
	-	Customer
	-	Lease
	-	IP Address
*/

-- Customer
SELECT
	customer_key as customerKey,
	'CUSTOMER' AS customerSortKey,
	first_name AS firstName,
	last_name AS lastName,
	email,
	gender,
	birthdate
FROM cdp.dbo.customer

-- Leases
SELECT
	customer_key AS customerKey,
	CONCAT('LEASE#',unit_id) AS customerSortKey,
	address,
	city,
	zip_code AS zipCode,
	type AS customerType,
	lease_terms AS leaseTerms,
	move_in_date AS moveInDate,
	move_out_date AS moveOutDate
FROM cdp.dbo.customer_lease;


CREATE TABLE cdp.dbo.customer_browsing_hist
(
	customer_key varchar(50),
	ip_address varchar(50),
	activity_timestamp varchar(50),
	activity_date varchar(50),
	app_name varchar(50),
	domain_name varchar(50),
	url varchar(50),
	top_level_domain varchar(50),
	user_agent varchar(255)
)

INSERT INTO cdp.dbo.customer_browsing_hist
SELECT * FROM cdp.dbo.browsing_hist1;

INSERT INTO cdp.dbo.customer_browsing_hist
SELECT * FROM cdp.dbo.browsing_hist2;

INSERT INTO cdp.dbo.customer_browsing_hist
SELECT * FROM cdp.dbo.browsing_hist3;

SELECT
	customer_key AS customerKey,
	CONCAT('BROWSEHIST#',ip_address,'-',activity_timestamp) AS customerSortKey,
	ip_address,
	activity_timestamp,
	activity_date,
	app_name,
	domain_name,
	url,
	top_level_domain,
	user_agent
FROM cdp.dbo.customer_browsing_hist