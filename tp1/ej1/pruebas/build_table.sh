#!/bin/bash
for filename in $@; do
	max_training=`cat "$filename" | awk 'NR == 1 {line = $0; max = $4}
		                   NR > 1 && $4 > max {line = $0; max = $4}
		                   END{print line}' | awk '{print $4,"("$1,"epochs)"}'`
	max_validation=`cat "$filename" | awk 'NR == 1 {line = $0; max = $5}
		                   NR > 1 && $5 > max {line = $0; max = $5}
		                   END{print line}' | awk '{print $5,"("$1,"epochs)"}'`
	echo -e "${max_training}\t${max_validation}"
done
