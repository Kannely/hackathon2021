Vue.component('skills', {
	template: `
	<div class="secondary-main">
		<nav class="secondary-nav">
			<ul v-for="(type_skills, type) in sorted_skills">
				<h3>{{ type }}</h3>
				<li v-for="skill in type_skills">
					<input type="radio" :id="skill.id" :value="skill.id" v-model="selected_skill" class="navbar-selection">
					<label :for="skill.id" class="navbar-selection">{{ skill.code }}</label>
				</li>
			</ul>
		</nav>
		<div class="div-margin">
			<skill-details :id="selected_skill"/>
		</div>
	</div>
	`,
	data: function() {
		return {
			skills: [],
			selected_skill: 1,
		}
	},
	computed: {
	    sorted_skills() {
	        let sorted_skills = {};
	        for (const skill of this.skills) {
	            if (!sorted_skills[skill.type]) sorted_skills[skill.type] = [];
	            let copied_skill = {...skill}; // Deep copy
	            delete copied_skill.type;
	            sorted_skills[skill.type].push(copied_skill);
	        }
	        return sorted_skills;
	    }
	},
	methods: {
		async searchSkills() {
			const response = await fetch(`/back/comp_list`);
			this.info = await response.json();
			for (let i = 0; i < this.info.length; i++) {
				const info_skill = this.info[i];
				const code = info_skill.code;
				let type;
				code.includes("G") == true ? type = "Compétences générales" : type = "Compétences techniques";
				const new_skill = {
				    id: info_skill.id,
				    code: code,
				    type: type
				};
				const skill_index = this.skills.findIndex(c => c.code == info_skill.code);
				if (skill_index > -1) Vue.set(this.skills, skill_index, new_skill);
				else this.skills.push(new_skill);			
			}
		}
	},
	mounted: function() {
		this.searchSkills();
	},
})

Vue.component('skill-details', {
	props: ["id"],
	template: `
	<div>
		<h1>{{ code }} - {{ name }}</h1>
		<h3>Description :</h3>
		<table id="skills-table">
			<tbody>
				<td>
					<ul id="skill-description" v-for="point in description">
						<li>{{ point }}</li>
					</ul>
				</td>
				<td><skill-levels-chart :data="seuils" :code="code" id="skills-chart"/></td>
			</tbody>
		</table>
		<table id="skill-details-table" class="info-table">
		<thead>
			<th>UE</th>
			<th>Période</th>
			<th>Niveau</th>
			<th>Jetons</th>
			<th>Evaluation</th>
		</thead>
		<tbody v-for="row in courses_details">
			<tr>
				<td>{{ row.code_ue }}</td>
				<td>{{ row.periode }}</td>
				<td>{{ row.niveau }}</td>
				<td>{{ row.jetons_valides }}</td>
				<td>{{ row.note }}</td>
			</tr>
		</tbody>
	</table>
	</div>
	`,
	data: function() {
		return {
			name: "",
			code: "",
			description: [],
			courses_details: [],
			seuils: Array(5).fill(0)
		}
	},
	methods: {
		async searchDetails() {
			const response = await fetch(`/back/comp/${this.id}`);
			this.info = await response.json();
			this.code = this.info.code;
			this.name = this.info.nom;
			this.description = this.info.description.split("* ").slice(1);

			for (let i = 0; i < this.info.ue_details.length; i++) {
			    let course = this.info.ue_details[i];
			    this.seuils[course.niveau-1]++;
				Vue.set(this.courses_details, i, course);
			}

		}
	},
	mounted: function() {
		this.searchDetails();
	},
	watch: {
		id() {
			this.searchDetails();
		}
	}
})

Vue.component('skill-levels-chart', {
	extends: VueChartJs.Bar,
	props: ["code", "data"],
	methods: {
		createChart() {
			this.renderChart({
				labels: ["Niveau 1", "Niveau 2", "Niveau 3", "Niveau 4", "Niveau 5"],
				datasets: [{
					label: this.code,
					backgroundColor: "#d2de81",
					data: this.data,

				}]
			}, {
         		scales: {
            		xAxes: [{
		                ticks: {
		                    autoSkip: false,
		                    maxRotation: 45,
		                    minRotation: 45,
		                }
            		}],
            		yAxes: [{
		                ticks: {
		                    stepSize: 1
		                }
            		}]
        		 }
			}, {
				responsive: true,
				maintainAspectRatio: false
			})
		},
		updateChart() {
			this._chart.destroy();
			this.createChart();
		}
	},
	mounted () {
		this.createChart();
	},
	watch: {
	    code() {
	        this.updateChart();
	    },
	    data() {
	        this.updateChart();
	    }
	}
})
