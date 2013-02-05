$(document).ready(function () {
    
    // TODO: only run this functionality when the browser is svg
    // compliant. Use modernizr?

    // TODO: use 'mousemove' event to detect mouse position and
    // d3.bisect to find nearest point. this might be a more intuitive
    // way to display the label.

    // This works by adding a transparent rectangle over the top of
    // the sparkline. On mouseover of the rectangle, we display the
    // .hover_info element

    // retrieve the data from the global variable and store it locally.
    var data = document.flux_sparkline_data;

    // get the counts from all of the data-count attributes on
    // .bin_inner and store them in a data array
    d3.selectAll(".flux_timeseries_container .flux_timeseries")
	.each(function (d, k){

	    var default_message = "";

	    // add the label box for each .flux_timeseries element
	    var hover_info = d3.select(this).insert("p", ":first-child")
	    	.attr("class", "hover_info")
		.html(default_message);

	    // get the height and width of the svg
	    var w, h;
	    var svg = d3.select(this).selectAll("svg").each(function () {
		w = $(this).width();
		h = $(this).height();
	    });

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