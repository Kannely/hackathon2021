Vue.component('obligations-table', {
	template: `
	<div id="obligations-table">
		<div v-if = "obligations!=null" v-for="obligation in obligations">
			{{obligation.name}}
			<div v-for="skill in obligation.skills">
				{{skill.name}}
			</div>
		</div>
	</div>
	`,
	data: function() {
		return {
			
		}
	},
	methods: {
		async searchObligations() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.obligations = [
				{
					name : 'Langues',
					skills : [
					{ name : 'LV1' },
					{ name : 'LV2' },
					{ name : 'IELTS' }
					]
				},
				{
					name : 'Expériences',
					skills : [
					{ name : 'Professionnelle' },
					{ name : 'A l\'étranger' }
					]
				}
			]
			
		}	
	},
	created: function() {
		this.searchObligations();
	}
})