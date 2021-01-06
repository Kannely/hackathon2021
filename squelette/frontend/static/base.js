/*const app = new Vue({
	el: '#app',
	delimiters: ["[[", "]]"],
	data: {
		favoriteCat: 'Berlioz'
	},
	computed: {
		label() {
			return 'New favorite cat : ' + this.favoriteCat
		}
	},
	methods: {
		alertCat(catName) {
			alert('My favorite cat is ' + catName);
		},
		changeCat() {
			this.favoriteCat = 'Garfield';
			this.alertCat(this.favoriteCat)
		}
	}
})*/

const movies = new Vue({
	el: '#app',
	delimiters: ["[[", "]]"],
	data: {
		actorName: 'Bruce',
		actorSurname: 'Willis',
	},
	computed: {
		label() {
			return 'Actor : ' + this.actorName + this.actorSurname
		}
	},
	methods: {
		alertActor(actorName, actorSurname) {
			alert('Actor : ' + actorName + ' ' + actorSurname);
		},
		searchMovies() {
			this.actorName = 'Matt';
			this.actorSurname = 'Damon';
			this.alertActor(this.actorName, this.actorSurname)
			movies(request, this.actorName, this.actorSurname)
		}
	}
})
// TODO : Change