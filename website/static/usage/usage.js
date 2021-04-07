$(function() {
	setInterval(function() {
		percent = Math.floor(Math.random() * 100);
		$("#gaugeLoad").attr("percent", percent);
		$("#gaugeLoad text.value tspan").text(percent + "%");
	}, 3000);

	setInterval(function() {
		percent = Math.floor(Math.random() * 100);
		$("#gaugeCPU").attr("percent", percent);
		$("#gaugeCPU text.value tspan").text(percent + "%");
	}, 6000);

	setInterval(function() {
		percent = Math.floor(Math.random() * 100);
		$("#gaugeRAM").attr("percent", percent);
		$("#gaugeRAM text.value tspan").text(percent + "%");
  }, 8000);

  setInterval(function() {
		percent = Math.floor(Math.random() * 100);
		$("#gaugeFlash").attr("percent", percent);
		$("#gaugeFlash text.value tspan").text(percent + "%");
  }, 6000);

  setInterval(function() {
		percent = Math.floor(Math.random() * 100);
		$("#gaugeStorage").attr("percent", percent);
		$("#gaugeStorage text.value tspan").text(percent + "%");
	}, 3000);

});