
import pdb
import sqlite3
# Connect to approrpiate database
connT = sqlite3.connect('training.db')
cuT = connT.cursor()
# import MATH.log to be used during analysis
import math
connT.create_function('log', 1, math.log)


def run_analysis(word_list):

	table_create(word_list)
	return execute()


def table_create(word_list):

	# Create table to put article words into
	cuT.execute('''
	    DROP TABLE newarticle
	''')

	cuT.execute('''
	    CREATE TABLE 
	        newarticle (word TEXT)
	''')

	for each in word_list:
	    cuT.execute('''
    	    INSERT INTO 
        	    newarticle (word) 
        	VALUES(?)'''
            	, (each,))

	print "new table generated"


def execute():

	ans = cuT.execute('''
    	SELECT
        	l.label,
	        (sum(l.loglike)+z.extr_count+log(p.clsprior)) as likely
	    FROM
	        log_likeval l
    JOIN
	        newarticle n ON n.word = l.word
	    JOIN
	        classprior p ON l.label = p.label
	    JOIN
	        (SELECT
	            l.label AS label,
	            (((SELECT count(*) FROM newarticle) - count(*))*(-10.5)) AS extr_count
 	       FROM
 	           log_likeval l
	        JOIN
	            newarticle n ON n.word = l.word
	        GROUP BY
	            l.label
	        ) z ON l.label = z.label
	    GROUP BY
	        l.label
	    ORDER BY
	        likely DESC
	''')

	#pdb.set_trace()

	full_results = ans.fetchall()
	print "analysis complete"

	top_results = "Prediction results (top 3, in order of higest to lowest): "
	for i in range(3):
		top_results = top_results + (" " + str(i+1) + ": " + full_results[i][0] + ",")

	return top_results
