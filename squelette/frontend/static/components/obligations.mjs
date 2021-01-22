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
				<tr v-for="skill in obligation.skills">
					<td>{{skill.name}}</td>
					<td>{{skill.current}}</td>
					<td>{{skill.objective}}</td>
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
					skills: [
					    { name: "ECTS", code: "ects" },
						{ name: "C2IO", code: "c2io" },
						{ name: "Compétences de niveau 3", code: "comp_nv3" }
					]
				},
				{
					name: 'Expériences',
					skills: [
						{ name: "Professionnelles", code: "stage" },
						{ name: "A l'étranger", code: "etranger" }
					]
				},
				{
					name: 'Langues',
					skills: [
						{ name: "IELTS", code: "ielts" },
						{ name: "LV1", code: "lv1" },
						{ name: "LV2", code: "lv2" }
					]
				},
			]
		}
	},
	methods: {
		async searchObligations() {
			const response = await fetch(`/back/obligations`);
			this.info = await response.json();
			for (let i = 0; i < this.obligations.length; i++) {
			    let obligation = this.obligations[i];
				for (let j = 0; j < obligation.skills.length; j++) {
					const skill = obligation.skills[j];
					obligation.skills[j] = {
					    ...skill,
					    current: this.info["etudiant"][skill.code],
					    objective: this.info["formation"][skill.code]
					};
				}
				Vue.set(this.obligations, i, obligation);
			}
		}	
	},
	mounted: function() {
		this.searchObligations();
	},
})
