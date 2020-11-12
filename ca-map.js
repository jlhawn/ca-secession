function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

class DataGroup extends Set {
	constructor(id, color, highlightColor) {
		super();
		this.id = id;
		this.color = color;
		this.highlightColor = highlightColor;
		this.next = null;
	}

	totalPopulation() {
		var population = 0;
		for (var county of this.values()) {
			population += county.population;
		}
		return population;
	}

	contestResults(contestID) {
		var results = {};
		for (var county of this.values()) {
			var contest = county.contests[contestID];
			for (var key in contest) {
				results[key] = results[key] || {count: 0, percent: 0, isWinner: false};
				results[key].count += contest[key];
			}
		}
		var totalCount = 0;
		var maxCount = 0;
		for (var key in results) {
			totalCount += results[key].count;
			maxCount = (results[key].count > maxCount ? results[key].count : maxCount);
		}
		for (var key in results) {
			results[key].percent = results[key].count / totalCount * 100;
			results[key].isWinner = results[key].count == maxCount;
		}
		return results;
	}

	render(contestID) {
		var container = document.getElementById(this.id);
		while (container.firstChild) {
			container.removeChild(container.firstChild);
		}
		if (this.size == 0) {
			container.style.display = "none";
			return;
		}

		container.style.display = "block";

		var tableElement = document.createElement("table");
		tableElement.style.borderLeftColor = this.color;
		container.appendChild(tableElement);

		var tableHeader = document.createElement("thead");
		tableElement.appendChild(tableHeader);

		var headRow = document.createElement("tr");
		tableHeader.appendChild(headRow);

		var th = document.createElement("th");
		th.setAttribute("colspan", 4);
		th.innerText = `Population: ${numberWithCommas(this.totalPopulation())}`;
		headRow.appendChild(th);

		var results = this.contestResults(contestID);
		var tableBody = document.createElement("tbody");
		tableElement.appendChild(tableBody);
		for (var key in results) {
			var result = results[key];

			var row = document.createElement("tr");
			tableBody.appendChild(row);

			var keyTd = document.createElement("td");
			keyTd.innerText = key;
			row.appendChild(keyTd);

			var winTd = document.createElement("td");
			winTd.innerText = result.isWinner ? "✔️" : "";
			row.appendChild(winTd);

			var countTd = document.createElement("td");
			countTd.innerText = `${numberWithCommas(result.count)}`;
			row.appendChild(countTd);

			var percentTd = document.createElement("td");
			percentTd.innerText = `${result.percent.toFixed(2)}%`;
			row.appendChild(percentTd);
		}
	}
}

class County {
	constructor(domElement, data, dataGroup, onChange) {
		this.domElement = domElement;
		this.name = data["name"];
		this.population = data["population"];
		this.contests = data["contests"];

		this.dataGroup = dataGroup;
		this.dataGroup.add(this);

		this.onChange = onChange;

		this.domElement.addEventListener("mousemove", this.onMouseMove.bind(this));
		this.domElement.addEventListener("mouseleave", this.onMouseLeave.bind(this));
		this.domElement.addEventListener("click", this.onClick.bind(this));

		this.onMouseLeave();
	}

	onMouseMove() {
		this.domElement.style.fill = this.dataGroup.highlightColor;
	}

	onMouseLeave() {
		this.domElement.style.fill = this.dataGroup.color;
	}

	onClick() {
		this.dataGroup.delete(this);
		this.dataGroup = this.dataGroup.next;
		this.dataGroup.add(this);
		this.onMouseMove();
		this.onChange();
	}
}

var dataGroupA = new DataGroup("data-group-a", "dodgerblue", "lightskyblue");
var dataGroupB = new DataGroup("data-group-b", "indianred", "lightcoral");
var dataGroupC = new DataGroup("data-group-c", "slateblue", "mediumslateblue");
var dataGroupD = new DataGroup("data-group-d", "seagreen", "mediumseagreen");

dataGroupA.next = dataGroupB;
dataGroupB.next = dataGroupC;
dataGroupC.next = dataGroupD;
dataGroupD.next = dataGroupA;

var dataGroups = [dataGroupA, dataGroupB, dataGroupC, dataGroupD];

function initialize(dataset) {
	var contestSelector = document.getElementById("contest");

	var renderDataGroups = function() {
		for (var dataGroup of dataGroups) {
			dataGroup.render(contestSelector.value);
		}
	}

	var graphic = document.getElementById("countymap_graphic");
	for (var domElement of graphic.children) {
		var countyID = domElement.dataset.info;
		var data = dataset[countyID];

		var county = new County(domElement, data, dataGroupA, renderDataGroups);
	}

	contestSelector.addEventListener("change", renderDataGroups);
	renderDataGroups();
}

window.addEventListener('DOMContentLoaded', (event) => {
    fetch("counties.json")
		.then(resp => resp.json())
		.then(dataset => initialize(dataset))
});

