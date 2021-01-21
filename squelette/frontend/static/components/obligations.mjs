Vue.component('obligations-table', {
	template: `
	<div class="div-margin">
		<table id="obligations-table" class="info-table">
			<thead>
				<th>Condition</th>
				<th>Etat actuel</th>
				<th>Objectif</th>
			</thead>
			<tbody v-for="obligation in obligations">
				<tr class="obligations-category">
					<td colspan="3">{{obligation.name}}</td>
				</tr>
				<tr v-for="(value,id) in obligation.skills">
					<td>{{value[0]}}</td>
					<td>{{value[1]}}</td>
					<td>{{value[2]}}</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data: function() {
		return {
			obligations: [
				{
					name: 'Général',
					skills: {
						ects: ["ECTS"],
						c2io: ["C2IO"],
						comp_nv3: ["Compétences de niveau 3"]
					}
				},
				{
					name: 'Expériences',
					skills: {
						stage: ["Professionnelles"],
						etranger: ["A l'étranger"]
					}
				},
				{
					name: 'Langues',
					skills: {
						ielts: ["IELTS"],
						lv1: ["LV1"],
						lv2: ["LV2"]
					}
				},
			]
		}
	},
	methods: {
		async searchObligations() {
			const response = await fetch(`/back/obligations`);
			this.info = await response.json();
			for (var i = 0; i < this.obligations.length; i++) {
				var skills = Object.keys(this.obligations[i].skills);
				for (var j = 0; j < skills.length; j++) {
					var skill = skills[j];
					this.obligations[i].skills[skill][1] = this.info["etudiant"][skill];
					this.obligations[i].skills[skill][2] = this.info["formation"][skill];

				}
			}
		console.log(this.obligations);
		}	
	},
	mounted: function() {
		this.searchObligations();
	},
	watch: {
	    obligations() {
	        console.log('hello');
	    }
	}
})
