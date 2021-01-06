Vue.component('cat-component', {
    template: `
    <div>
        <p>{{ label }}</p>
        <button @click="alert()">Alert</button>
        <input type="text" v-model="favoriteCat" />
    </div>
    `,
	data: function() {
	    return {
		    favoriteCat: 'Berlioz'
		}
	},
	computed: {
		label() {
			return this.formatCat(this.favoriteCat)
		}
	},
	methods: {
	    formatCat(cat) {
	        return `My favorite cat is ${cat}.`
	    },
		alert() {
			alert(this.formatCat(this.favoriteCat))
		}
	}
})
