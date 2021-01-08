import { debounce } from './utils/general.mjs';

Vue.component('movies-component', {
	template: `
	<div class="center">
		<input type="text" v-model="actorName"/>
		<input type="text" v-model="actorSurname"/>
		<button @click="searchMovies()">Force search</button>
		<h3>Movies starring {{ actorName }} {{ actorSurname }} : </h3>
		<input id="filter-input" type="text" v-model="filter" placeholder="Filter movies"/>
		<table id="movie-table">
			<tbody v-if="movies.length > 0">
				<tr v-for="(row, index) in filteredRows">
					<td v-html="highlightMatches(row)"></td>
				</tr>
			</tbody>
			<tbody v-else>
				<tr>
					<td>None...</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	data: function() {
		return {
			actorName: 'Bruce',
			actorSurname: 'Willis',
			movies: [],
			filter: ''
		}
	},
	computed: {
		label() {
			return this.formatActor(this.actorName, this.actorSurname);
		},
		filteredRows() {
			return this.movies.filter(row => {
				const title = row.toString().toLowerCase();
				const searchTerm = this.filter.toLowerCase();
				return title.includes(searchTerm);
			});
		}
	},
	methods: {
		formatActor(actorName, actorSurname) {
			return `Actor : ${actorName} ${actorSurname}.`;
		},
		async searchMovies() {
			const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.movies = await response.json();
		},
		highlightMatches(text) {
			const matchExists = text.toLowerCase().includes(this.filter.toLowerCase());
			if (!matchExists) return text;

			const re = new RegExp(this.filter, 'ig');
			return text.replace(re, matchedText => `<strong>${matchedText}</strong>`);
		}		
	},
	created: function() {
		this.debouncedSearchMovies = debounce(this.searchMovies, 500)
		this.searchMovies();
	},
	watch: {
		actorName() {
			this.debouncedSearchMovies();
		},
		actorSurname() {
			this.debouncedSearchMovies();
		}
	}
})
