// convert the bar charts into sparklines
$(document).ready(function () {
    
    // add an element to the DOM to display the label 

    // get the counts from all of the data-count attributes on
    // .bin_inner and store them in a data array
    var data = [];
    d3.selectAll(".flux_timeseries_container .flux_timeseries .timeseries")
	.each(function (d, i){

	    var default_message = "";

	    // add the label box for each .timeseries
	    var hover_info = d3.select(this).insert("p", ":first-child")
	    	.attr("class", "hover_info")
		.html(default_message);

	    // display a label on mouseover for every .bin_outer 
	    d3.select(this).selectAll(".bin_outer").each(function (e, j) {
		d3.select(this).on("mouseover", function (d, i){
		    d3.select(this).select(".bin_inner").datum(function () {
			hover_info.html(this.dataset["count"]);
		    });
		}).on("mouseout", function (d, i){
		    d3.select(this).select(".bin_inner").datum(function () {
			hover_info.html(default_message);
		    });
		});
	    });
	});

});