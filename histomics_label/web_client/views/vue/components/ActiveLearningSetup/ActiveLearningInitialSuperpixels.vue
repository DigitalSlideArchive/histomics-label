<script>
import Vue from 'vue';

import { activeLearningSteps } from '../constants.js';

import { store } from '../store.js';

export default Vue.extend({
    props: ['backboneParent', 'certaintyMetrics', 'featureShapes'],
    computed: {
        validForm() {
            return this.radius > 0 && this.magnification > 0;
        },
        radius: {
            get() {
                return store.initialTrainingParameters.radius || 100;
            },
            set(value) {
                store.initialTrainingParameters.radius = value;
            }
        },
        magnification: {
            get() {
                return store.initialTrainingParameters.magnification || 5;
            },
            set(value) {
                store.initialTrainingParameters.magnification = value;
            }
        },
        certaintyChoice: {
            get() {
                return store.initialTrainingParameters.certainty;
            },
            set(value) {
                store.initialTrainingParameters.certainty = value;
            }
        },
        featureChoice: {
            get() {
                return store.initialTrainingParameters.feature;
            },
            set(value) {
                store.initialTrainingParameters.feature = value;
            }
        }
    },
    mounted() {
        this.certaintyChoice = this.certaintyMetrics[0];
        this.featureChoice = this.featureShapes[0];
    },
    methods: {
        initialTraining() {
            store.activeLearningStep = activeLearningSteps.InitialLabeling;
            store.initialTrainingParameters = {
                radius: this.radius,
                magnification: this.magnification,
                certainty: this.certaintyChoice,
                feature: this.featureChoice
            };
            this.backboneParent.initialTraining();
            this.backboneParent.updateHistomicsYamlConfig();
        }
    }
});
</script>

<template>
  <div class="h-al-setup-superpixels">
    <div class="form-group">
      <label for="radius">Superpixel Radius</label>
      <div class="form-group-description">
        Approximate superpixel radius
      </div>
      <input
        id="radius"
        v-model.number="radius"
        class="form-control input-sm h-active-learning-input"
        type="number"
      >
    </div>
    <div class="form-group">
      <label for="magnification">Magnification</label>
      <div class="form-group-description">
        Image magnification for superpixel generation
      </div>
      <input
        id="magnification"
        v-model.number="magnification"
        class="form-control input-sm h-active-learning-input"
        type="number"
      >
    </div>
    <div class="form-group">
      <label for="certainty-metric">Certainty Metric</label>
      <div class="form-group-description">
        Metric to determine the order that predictions are presented to the user
      </div>
      <select
        id="certainty-metric"
        v-model="certaintyChoice"
      >
        <option
          v-for="option in certaintyMetrics"
          :key="option"
          :value="option"
        >
          {{ option }}
        </option>
      </select>
    </div>
    <div class="form-group">
      <label for="feature-shape">Feature Shape</label>
      <div class="form-group-description">
        Feature is superpixel image data or foundation model vector
      </div>
      <select
        id="feature-shape"
        v-model="featureChoice"
      >
        <option
          v-for="option in featureShapes"
          :key="option"
          :value="option"
        >
          {{ option }}
        </option>
      </select>
    </div>
    <button
      class="btn btn-primary h-generate-superpixel-btn"
      :disabled="!validForm"
      @click="initialTraining"
    >
      Generate Superpixels
    </button>
  </div>
</template>

<style scoped>
.h-active-learning-input {
    width: 30%;
}

.h-generate-superpixel-btn {
    display: block;
}

.h-al-setup-superpixels {
    margin-left: 10px;
}
</style>
