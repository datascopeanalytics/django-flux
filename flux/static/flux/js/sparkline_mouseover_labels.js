$(document).ready(function () {
    
    // TODO: only run this functionality when the browser is svg
    // compliant. Use modernizr?

    // This works by adding a transparent rectangle over the top of
    // the sparkline. On mouseover of the rectangle, we display the
    // .hover_info element

    // retrieve the data from the global variable and store it locally.
    var data = document.flux_sparkline_data;

    // get the counts from all of the data-count attributes on
    // .bin_inner and store them in a data array
    d3.selectAll(".flux_timeseries_container .flux_timeseries")
	.each(function (d, k){

	    var default_message = "hello";

	    // add the label box for each .flux_timeseries element
	    var hover_info = d3.select(this).insert("p", ":first-child")
	    	.attr("class", "hover_info")
		.html(default_message);

	    // map the index of the element in the data array to the
	    // width of the svg
	    var w = $(this).width();

	    // map the value of the element in the data array to the
	    // height of the svg
	    var h = $(this).height();

	    // add the transparent rectangle
	    d3.select(this).selectAll(".timeseries.sparkline")
		.selectAll(".hover_rect")
		.data(data[k]).enter()
		.append("rect")
		.attr("x", function (d, i) {return i/data[k].length * w;})
		.attr("y", 0)
		.attr("width", w / data[k].length)
		.attr("height", h)
		.attr("fill", "black")
		.attr("fill-opacity", 0)
		.attr("stroke", "none")
		.on("mouseover", function (d, i) {
		    hover_info.html(data[k][i]);
		}).on("mouseout", function (d, i) {
		    hover_info.html(default_message);
		});

	});
});