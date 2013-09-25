// cmds.js - Ajax interface to sysinfo project.

// Utilities

function display_array(sel, array) {
        $(sel).empty();
	$.each(array, function (i, x) {
		$(sel).append('<div>' + x + '</div>');
	});
}

function display_obj(sel, obj) {
        $(sel).empty();
	$.each(obj, function (k, v) {
		var value = v === '' ? '--' : v;
		$(sel).append('<div><span class="bold">'
			+ k + ": </span><span>" + value + '</span></div>');
	});
}

function notify(msgs, severity) {
	var severity = severity || 'error';
	var sel = '#notifications';
	$(sel).empty();
	$.each(msgs, function (i, x) {
		$(sel).append('<div class="' + severity + '">'
			+ '<span class="bold">'
                        + severity.toUpperCase() + ': </span>'
                        + x + '</div>');
	});
}

function meter(level) {
	$('.meter > span').css('width', level);
}


// Command factory

function Command(prms) {

	function check(res, k) {
		if (res['errors']) {
			notify(res['errors'], 'error');
		} else {
			$('#notifications > .error').remove();
		}	
		if (res['warnings']) {
			notify(res['warnings'], 'warning');
		} else {
			$('#notifications > .warning').remove();
		}
		if (res['data']) {
			k(res['data']);
		} else {
			notify('Data not avaliable', 'error');
		}
	}

	return function(args) {
		$.ajax({
			url: prms.url,
			type: prms.type,
			dataType: 'json',
			data: args,
			success: function (r) {
				check(r, prms.fn);
			},
			error: function(jqxhr, text, error) {
				notify([error]);
			},
		});
	};
}


// Commands.

var cmds = (function () {

	var definitions = {
		battery: {
			url: 'api/battery',
			type: 'GET',
			fn: function(data) {
				display_obj('#content', data);
				meter(data['level']);
			}
		},
		wifi: {
			url: 'api/wifi',
			type: 'GET',
			fn: function(data) {
				display_array('#content', data);
			}
		}
	};

	var cmds = {};
	for (k in definitions) {
		cmds[k] = Command(definitions[k]);
	}
	return cmds;
})();

