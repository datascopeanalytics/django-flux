$(document).ready(function () {
    
    // TODO: only run this functionality when the browser is svg
    // compliant. Use modernizr?


    // get the counts from all of the data-count attributes on
    // .bin_inner and store them in a data array and also globally in
    // document.flux_sparkline_data for optionally adding labels on
    // mouseover.
    var data = [];
    document.flux_sparkline_data = data;
    d3.selectAll(".flux_timeseries_container .flux_timeseries .timeseries")
	.each(function (d, i){
	    data.push([]);
	    d3.select(this).selectAll(".bin_inner").datum(function () {
		data[data.length-1].push({
		    "count": Number(this.dataset["count"]),
		    "beg": new Date(this.dataset["beg"]),
		    "end": new Date(this.dataset["end"])
		});
	});
    });

    // remove all of the existing timeseries divs from the DOM
    d3.selectAll(".flux_timeseries_container .flux_timeseries .timeseries")
    	.remove();
    
    // add the timeseries spark line to the data. inspiration from
    // http://bl.ocks.org/1133472
    d3.selectAll(".flux_timeseries_container .flux_timeseries")
    	.append("svg")
    	.attr("class", "timeseries sparkline").each(function (d, k) {

    	    // map the index of the element in the data array to the
    	    // width of the svg
    	    var x = d3.scale.linear()
    		.domain([0, data[k].length])
    		.range([0, $(this).width()]);

    	    // map the value of the element in the data array to the
    	    // height of the svg
    	    var y = d3.scale.linear()
    		.domain([d3.max(data[k].map(function (d) {return d.count})), 0])
    		.range([0, $(this).height()]);

    	    // create a line path from the data
    	    var line = d3.svg.line().x(function (d, i) {
    		return x(i+0.5);
    	    }).y(function (d, i) {
    		return y(d.count);
    	    });

    	    // add the sparkline to the DOM
    	    d3.select(this)
    		.append("svg:path")
    		.attr("d", line(data[k]));

    });

    // change the display to show the timeseries sparklines. By
    // default, the .flux_timeseries divs are display:none in the
    // CSS. Displaying everything at the end avoids problems with
    // flashing
    d3.selectAll(".flux_timeseries_container .flux_timeseries")
    	.style("display", "inline");

});