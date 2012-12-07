// convert the bar charts into sparklines
$(document).ready(function () {
    
    // TODO: only run this functionality when the browser is svg
    // compliant. Use modernizr?


    // get the counts from all of the data-count attributes on
    // .bin_inner and store them in a data array
    var data = [];
    d3.selectAll(".flux_timeseries_container .flux_timeseries .timeseries")
	.each(function (d, i){
	    data.push([]);
	    d3.select(this).selectAll(".bin_inner").datum(function () {
		data[data.length-1].push(Number(this.dataset["count"]));
	});
    });

    // remove all of the existing timeseries data
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
		.domain([d3.max(data[k]), 0])
		.range([0, $(this).height()]);

	    // create a line path from the data
	    var line = d3.svg.line().x(function (d, i) {
		return x(i+0.5);
	    }).y(function (d, i) {
		return y(d);
	    });

	    d3.select(this).append("svg:path").attr("d", line(data[k]));

    });
});