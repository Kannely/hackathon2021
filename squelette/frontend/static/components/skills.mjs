Vue.component('skills', {
	template: `
	<div class="div-margin">
		<nav class="nav-two">
			<div>
				<ul v-for="(type_skills, type) in sorted_skills">
					<li><h3>{{ type }}</h3></li>
					<ul v-for="skill in type_skills">
						<li>
							<input type="radio" :id="skill.id" :value="skill.id" v-model="selected_skill" class="navbar-selection" @change="updateSkill()">
							<label :for="skill.id" class="navbar-selection">{{ skill.code }}</label>
						</li>
					</ul>
				</ul>
			</div>
		</nav>
		<div style="margin-left: 200px;">
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
		},
		updateSkill() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			//this.info = await response.json();
			this.name = 'Hackathon';
			this.description = 'On va vous en mettre plein la vue !';
			this.teacher = 'Hervé GRALL';
		}
	},
	mounted: function() {
		this.searchSkills();
	},
})

Vue.component('skill-details', {
	props: ["id"],
	template: `
	<div class="div-margin">
		<h1>{{ code }} - {{ name }}</h1>
		<table id="skills-table">
			<tbody>
				<td>
					<h3>Description :</h3>
						<ul v-for="point in description">
							<li>{{ point }}</li>
						</ul>
				</td>
				<td><skill-levels-chart :code="picked" :data="data" style="height: 200px;"/></td>
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
			courses_details: []
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
				Vue.set(this.courses_details, i, course);
			}
			console.log(this.courses_details);
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
