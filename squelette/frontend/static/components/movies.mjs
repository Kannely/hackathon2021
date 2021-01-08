import { debounce } from './utils/general.mjs';

Vue.component('movies-component', {
    template: `
    <div>
        <input type="text" v-model="actorName"/>
        <input type="text" v-model="actorSurname"/>
        <button @click="searchMovies()">Force search</button>
        <h3>Movies starring {{ actorName }} {{ actorSurname }} : </h3>
        <table id="movie-table">
            <tbody v-if="movies.length > 0">
                <tr v-for="movie in movies">
	                <td>{{ movie }}</td>
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
	    }
	},
	computed: {
		label() {
			return this.formatActor(this.actorName, this.actorSurname);
		}
	},
	methods: {
	    formatActor(actorName, actorSurname) {
	        return `Actor : ${actorName} ${actorSurname}.`;
	    },
		alertActor() {
			alert(this.formatActor(this.actorName, this.actorSurname));
		},
		async searchMovies() {
		    const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
		    this.movies = await response.json();
	    },
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
