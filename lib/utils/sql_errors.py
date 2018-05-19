#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re

sql_errors = {
	'MySQL': (
		r'SQL syntax.*MySQL',
		r'Warning.*mysql_.*',
		r'MySqlException \(0x"',
		r'valid MySQL result',
		r'check the manual that corresponds to your (MySQL|MariaDB) server version',
		r'MySqlClient\.',
		r'com\.mysql\.jdbcd\.exceptions',
		),
	'DB2':(
		r'CLI Driver.*DB2","DB2 SQL error',
		r'\bdb2_\w+\(","SQLSTATE.+SQLCODE',
		),
	'Firebird':(
		r'Dynamic SQL Error',
		r'Warning.*ibase_.*',
		),
	'HSQLDB':(
		r'org\.hsqldb\.jdbc',
		r'Unexpected end of command in statement \[',
		r'Unexpected token.*in statement \[',
		),
	'Informix':(
		r'Exception.*Informix',
		r'Informix ODBC Driver',
		r'com\.informix\.jdbc',
		r'weblogic\.jdbc\.informix',
		),
	'Ingres':(
		r'Warning.*ingres_',
		r'Ingres SQLSTATE',
		r'Ingres\W.*Driver',
		),
	'Microsoft Access':(
		r'Microsoft Access (\d+ )?Driver',
		r'JET Database Engine',
		r'Access Database Engine',
		r'ODBC Microsoft Access',
		r'Syntax error \(missing operator\) in query expression',
		),
	'SAP MaxDB':(
		r'SQL error.*POS([0-9]+).*',
		r'Warning.*maxdb.*',
		),
	'MsSQL':(
		r'Driver.* SQL[\-\_\ ]*Server',
		r'OLE DB.* SQL Server',
		r'\bSQL Server[^&lt;&quot;]+Driver',
		r'\bSQL Server[^&&]+Driver',
		r'Warning.*(mssql|sqlsrv)_',
		r'\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}',
		r'\bSQL Server[^&&]+[0-9a-fA-F]{8}',
		r'System\.Data\.SqlClient\.SqlException',
		r'(?s)Exception.*\WRoadhouse\.Cms\.',
		r'Microsoft SQL Native Client error \'[0-9a-fA-F]{8}',
		r'com\.microsoft\.sqlserver\.jdbc\.SQLServerException',
		r'ODBC SQL Server Driver',
		r'SQLServer JDBC Driver',
		r'macromedia\.jdbc\.sqlserver',
		r'com\.jnetdirect\.jsql',
		),
	'Oracle':(
		r'\bORA-\d{5}',
		r'Oracle error',
		r'Oracle.*Driver',
		r'Warning.*\Woci_.*',
		r'Warning.*\Wora_.*',
		r'oracle\.jdbc\.driver',
		r'quoted string not properly terminated',
		),
	'PostgreSQL':(
		r'PostgreSQL.*ERROR',
		r'Warning.*\Wpg_.*',
		r'valid PostgreSQL result',
		r'Npgsql\.',
		r'PG\:\:SyntaxError\:',
		r'org\.postgresql\.util\.PSQLException',
		r'ERROR:\s\ssyntax error at or near',
		),
	'SQLite':(
		r'SQLite/JDBCDriver',
		r'SQLite\.Exception',
		r'System\.Data\.SQLite\.SQLiteException',
		r'Warning.*sqlite_.*',
		r'Warning.*SQLite3\:\:',
		r'\[SQLITE_ERROR\]',
		),
	'Sybase':(
		r'Warning.*sybase.*',
		r'Sybase message',
		r'Sybase.*Server message.*',
		r'SybSQLException',
		r'com\.sybase\.jdbc',
		)
}

def sql_error(content):
	for key in sql_errors.keys():
		dbms = sql_errors[key]
		for error in dbms:
			if re.search(error,content):
				return (key,error)
	return (None,None)