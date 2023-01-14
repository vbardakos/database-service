(
	SELECT
		TRUE AS is_version,
		CASE
			WHEN installed_rank > %(lock)s THEN installed_rank
		END AS vid,
		md5(string_agg(md5(script || CAST(checksum AS text)), '')) AS vhash
	FROM %(_schema)s.flyway_schema_history
	WHERE VERSION IS NOT NULL
	GROUP BY vid
) UNION ALL (
	SELECT
		FALSE AS is_version,
		installed_rank AS vid,
		md5(script || CAST(checksum AS TEXT)) AS vhash
	FROM %(_schema)s.flyway_schema_history
	WHERE VERSION IS NULL AND installed_rank > 0
);
