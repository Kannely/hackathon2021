Vue.component('obligations-table', {
	template: `
	<div>
		<table id="obligations-table">
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
					<td>{{skill.currently}}</td>
					<td>{{skill.goal}}</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data: function() {
		return {
			
		}
	},
	methods: {
		searchObligations() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.obligations = [
				{
					name : 'Langues',
					skills : [
					{
						name : 'LV1',
						currently : 'B2',
						goal : 'C1'
					},
					{
						name : 'LV2',
						currently : 'B2',
						goal : 'B2'
					},
					{
						name : 'IELTS',
						currently : 'N/A',
						goal : '7.5/9'
					}
					]
				},
				{
					name : 'Expériences',
					skills : [
					{
						name : 'Professionnelle',
						currently : '10 mois',
						goal : '18 mois'
					},
					{
						name : 'A l\'étranger',
						currently : '5 mois',
						goal : '9 mois'
					}
					]
				}
			]
			
		}	
	},
	created: function() {
		this.searchObligations();
	}
})