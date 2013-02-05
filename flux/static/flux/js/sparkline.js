// create a global variable to store the bottom margin of the svg so
// that the sparkline_mouseover_labels.js script can see the same
// boundary
document.flux_bottom_margin = 10;

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
	    var w = $(this).width();
    	    var x = d3.scale.linear()
    		.domain([0, data[k].length])
    		.range([0, w]);
	    var t = d3.time.scale()
    		.domain([data[k][0].beg, data[k][data[k].length-1].end])
    		.range([0, w]);

    	    // map the value of the element in the data array to the
    	    // height of the svg
	    var h = $(this).height();
	    var margin = document.flux_bottom_margin;
    	    var y = d3.scale.linear()
    		.domain([d3.max(data[k].map(function (d) {return d.count})), 0])
    		.range([0, h-margin]);

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

	    // add the time axis to the DOM. useful links:
	    // http://jsfiddle.net/robdodson/KWRxW/
	    // https://github.com/mbostock/d3/wiki/Time-Formatting
	    var format = d3.time.format('%b');
	    function tick_format (d, i) {
		return format(d, i).substr(0,1)
	    }
	    tAxis = d3.svg.axis()
		.scale(t)
		.orient('bottom')
		.ticks(d3.time.months, 1)
		.tickFormat(tick_format)
		.tickSize(0)
		.tickPadding(3);
	    d3.select(this)
		.append('g')
		.attr('class', 't axis')
		.attr('transform', 'translate(0, ' + (h - margin)+')')
		.call(tAxis);

    });

    // change the display to show the timeseries sparklines. By
    // default, the .flux_timeseries divs are display:none in the
    // CSS. Displaying everything at the end avoids problems with
    // flashing
    d3.selectAll(".flux_timeseries_container .flux_timeseries")
    	.style("display", "inline");

});