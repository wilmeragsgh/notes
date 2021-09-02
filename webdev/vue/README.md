---
description: Some notes on vue
---

# Vue

## Some directives

`v-html`: It's a bind for interpreting the passed vould from js expression as html.

```html
<p v-html="func1()"></p>
```



`v-bind:href`: It's an example of a bind for setting html properties based on vue outputs.

```html
<a :href="dynamicHref"></a>
```

`v-once`: any dynamic binding gets used only the first time

`v-for="elem in eleList"`: It's an example of an iterator directive for vue elements.

`@click.enter`: It's an example of event modifier where we edit the click event

`@submit.prevent`: Prevent browser from refresh the page on submit button

`v-model='data'`is equivalent to `v-bind:value=data` `v-on:input="setData($event)"` where you bind the data for an input for example

To use an event data we can refer to event into the function parameters, then access its data, like:

```html
<input @keydown="eventName">
</input>
```

```js
eventName() {
	this.varMe = event.target.value;
}
```

alternatively,

```vue
<input ref="refName">
</input>
```

then,

```js
eventName() {//trigger at a given point
	this.varMe = this.$refs.refName;
}
```



Most of the times you want to use computed instead of methods to avoid unnecesary recalculations(computed keep track of execution dependencies)

## Kickstarting code

```javascript
# Sample kickstarting code for a vue application (app.js)
Vue.createApp({
    data() {
        return {
            obj1: "Hello world"
        }
    },
    methods: {
        fun1() {
            return Math.random()
        }
    },
    computed: { // no params required and only re-executed 
        fun2() {
            return ''
        }
    },
    watch: { // If a value or computed property change
        fun2: obj1(value oldValue) {
            return '' //Perform operation when obj data value changes
        }
    }
}).mount("#app");
```

```html
<div id="app">
    <p>
        {{ obj1 }}
    </p>
    <p>
        {{ fun2 }}
    </p>
</div>
```

- Vue re-execute all methods inserted in the html so methods are not the best solution for outputing dynamicly calculated values

- computed properties are not inserted as methods '()' only referenced so vue call them

- Vue detects dependencies on computed properties to trigger its re-execution.

- v-on  can be substituted by `@`

- v-bind:value can be substitued by `:value`

  ![image-20210408220726578](/home/w/.config/Typora/typora-user-images/image-20210408220726578.png)



Style binding:

`:style="borderColor: attr ? 'red': '#ccc'"` ternary expression, but is dangerous bc it can override css classes, for classes:

`:class="{demo: true, active: attrAct}"` here if attrAct is true then active class is also used,

the `{demo:true, active: attrAct}` could be the returned value of a computed property. Can't also be an array of the shape: `['demo', {active: attrAct}]`



`v-if="condition"` can be use for conditional showing

**Right after v-if**,  `v-else` or `v-else-if="newCondition"` can be use as complement



User `v-show` only if visisbility state changes a lot.



`v-for` can be used for iterating on objects like `v-for=(value, key, index) in {key1: 'v1', key2: 'v2'}` , remember to use `:key="goal"` where goal is is a unique reference to each element in the list iterate over in the `v-for`

![image-20210408220537910](/home/w/.config/Typora/typora-user-images/image-20210408220537910.png)

An event that want to be stopped in children propagations can be achieved by `@event.stop`

Remember to use.



Other hooks can be added to the vue app as:

![image-20210425221524014](/home/w/.config/Typora/typora-user-images/image-20210425221524014.png)

They're added as syblings to data or methods

## Components

```js
app.component('component-name', {
    template: `html`,
    data () {
        return {id: 1}
    },
    methods () {
        m1 () {
            return 1;
        }
    }
})
```



## Tools

- https://github.com/vuegg/vuegg
- https://mui.dev/
- https://cli.vuejs.org/
- https://vuetifyjs.com/en/getting-started/installation/
- https://vuex.vuejs.org/
- https://element-plus.org/#/en-US
- https://bootstrap-vue.org/docs/components
- https://youzan.github.io/vant/#/en-US/
- https://quasar.dev/
- https://www.vue-tailwind.com/
- https://github.com/mchandleraz/realworld-vue
- https://vuetifyjs.com/en/getting-started/wireframes/
- https://buefy.org/
- https://vue.mdbootstrap.com/#/
- https://github.com/PanJiaChen/vue-element-admin
- https://vuejsexamples.com/tag/admin-template/
- https://github.com/antoine92190/vue-advanced-chat
- https://vuesax.com/
- https://nuxtjs.org/
- https://tailwindui.com/pricing

## References

- https://vuejs.org/v2/guide/
- https://vuejs.org/v2/style-guide/
- https://router.vuejs.org/installation.html#direct-download-cdn
- https://www.jenniferbland.com/spa-application-using-vue-js-vuex-vuetify-and-firebase-part-1/
- https://www.jenniferbland.com/spa-application-using-vue-js-vuex-vuetify-and-firebase-part-2/
- https://www.jenniferbland.com/spa-application-using-vue-js-vuex-vuetify-and-firebase-part-3/
- https://www.jenniferbland.com/spa-application-using-vue-js-vuex-vuetify-and-firebase-part-4/
- https://itnext.io/how-to-structure-a-vue-js-project-29e4ddc1aeeb
- https://dev.to/mornir/add-tailwind-to-your-vue-app-5hea
- https://medium.com/front-end-weekly/from-vuetify-to-tailwind-a7e83284ddfc
- https://www.reddit.com/r/vuejs/comments/g4gpwb/vue_js_or_nuxt_vuetify_or_bootstraptailwind_etc/
- 