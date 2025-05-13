<template>
  <div id="app">
    <h1>Family Tree</h1>
    <div class="container">
      <div class="text-section">
        <h2>Family Tree Summary</h2>
        <pre>{{ familyTreeText }}</pre>
        <button @click="loadFamilyTreeText">Refresh Text</button>
        <hr />
        <h2>Edit poparan.txt</h2>
        <button @click="loadPoparan" :disabled="editingPoparan">Load poparan.txt</button>
        <div v-if="editingPoparan">
          <textarea v-model="poparanContent" rows="15" style="width: 100%;"></textarea>
          <button @click="savePoparan">Save poparan.txt</button>
          <button @click="generateFamilyTree" :disabled="loadingGenerate">
            {{ loadingGenerate ? 'Generating...' : 'Generate Family Tree' }}
          </button>
          <p>{{ message }}</p>
        </div>
      </div>
      <div class="image-section">
        <h2>Family Tree Images</h2>
        <h3>Landscape</h3>
        <div class="image-zoom-container">
          <img
            :src="landscapeImage"
            alt="Family Tree Landscape"
            :style="{ transform: `scale(${landscapeZoom})` }"
          />
          <div class="zoom-controls">
            <button @click="zoomIn('landscape')">+</button>
            <button @click="zoomOut('landscape')">-</button>
            <span>{{ Math.round(landscapeZoom * 100) }}%</span>
          </div>
        </div>
        <h3>Portrait</h3>
        <div class="image-zoom-container">
          <img
            :src="portraitImage"
            alt="Family Tree Portrait"
            :style="{ transform: `scale(${portraitZoom})` }"
          />
          <div class="zoom-controls">
            <button @click="zoomIn('portrait')">+</button>
            <button @click="zoomOut('portrait')">-</button>
            <span>{{ Math.round(portraitZoom * 100) }}%</span>
          </div>
        </div>
        <button @click="refreshImages">Refresh Images</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      familyTreeText: '',
      landscapeImage: '/family_tree_landscape.png',
      portraitImage: '/family_tree_portrait.png',
      timestamp: Date.now(),
      landscapeZoom: 1,
      portraitZoom: 1,
      editingPoparan: false,
      poparanContent: '',
      loadingGenerate: false,
      message: ''
    }
  },
  methods: {
    loadFamilyTreeText() {
      this.familyTreeText = `OSMAR SAMOSIR (†) - TIORA br GULTOM (OP. SANTOSO HOSPITAL SAMOSIR)
  RUSMAN SAMOSIR - GLORIA br GULTOM (†) - ERTINA br GULTOM
    SANTOSO HOSPITAL SAMOSIR
    SAMOS SAMOSIR
    SANNI br SAMOSIR
    SATRIO SAMOSIR
    SAHAYA br SAMOSIR
    SIVA SAMOSIR
  JUSMAN LEONARDO SAMOSIR (†) - NURMALA br SAGALA (†) - ESSY br NAPITUPULU
    MULIA SAMOSIR - VERONICA br SAGALA
      TESALONIKA br SAMOSIR
    LIAN SAMOSIR
    JOSUA SAMOSIR
    SION SAMOSIR
    YEHEZKIEL KEDESH SAMOSIR
    ALCANDER SAMOSIR
  HATMAN SAMOSIR
  BUDI SAMOSIR - PAULINA br SIANIPAR
    YOHANA br SAMOSIR - RUDOL SIHOTANG
      PUTRA SIHOTANG
      DEWI br SIHOTANG
      RISKI SIHOTANG
    SUHADI SAMOSIR (†)
    LABETUDU SAMOSIR - ARTA ULI br SITORUS
  MANGATAR SAMOSIR - ERNITA br GULTOM
    JOEL SAPUTRA SAMOSIR - LESTARI br GULTOM
      MAYLIKA br SAMOSIR
      VELISYA br SAMOSIR
      IREN CLAUDIA br SAMOSIR
      ROMARITO br SAMOSIR
    YANTI WIDAYANI br SAMOSIR - RUWINDO SINAGA
  St. PITUA SAMOSIR - ELRITA br HUTAGALUNG
    DANIEL RAFFIANDO SAMOSIR
    THALIA GEBRIELLA br SAMOSIR
  HARIANTO SAMOSIR - br HABEAHAN
    HELEN WULANDARI br SAMOSIR
    ALEXANDER HENDI SAPUTRA SAMOSIR
    KRISNA IMMANUEL SAMOSIR
  ANGGIAT SIMORANGKIR - SETIANA RITA br SAMOSIR (†)
    MURNI KASIH br SIMORANGKIR - UCOK HANSEN SITINJAK
      ADRIAN SITINJAK
    DIAN PUTRI br SIMORANGKIR - AMIN
    LIDIA TIATIRA br SIMORANGKIR
    GIF SIMORANGKIR
    JOGI SIMORANGKIR
    DOLI SIMORANGKIR
    WIN AYU br SIMORANGKIR
  USRIN MALAU - GOLDA LUMBANRAJA - BUNGAULI br SAMOSIR
    PRENGKI MALAU
    EGI MALAU
    MARITO MALAU
    MARIATI br MALAU
    ULI br MALAU
    ANDORMAN LUMBANRAJA
    ROIMAN LUMBANRAJA
    VANJI LUMBANRAJA - br PARHUSIP
      EDITA br LUMBANRAJA
    WANSEP LUMBANRAJA
    JOHANNES LUMBANRAJA
    RINDA LUMBANRAJA
    BELZANO LUMBANRAJA
    ULI WIRANARIA br LUMBANRAJA
    MARTA br LUMBANRAJA`
    },
    refreshImages() {
      this.timestamp = Date.now()
      this.landscapeImage = `/family_tree_landscape.png?t=${this.timestamp}`
      this.portraitImage = `/family_tree_portrait.png?t=${this.timestamp}`
      this.landscapeZoom = 1
      this.portraitZoom = 1
    },
    zoomIn(image) {
      if (image === 'landscape' && this.landscapeZoom < 5) {
        this.landscapeZoom = Math.min(this.landscapeZoom + 0.1, 5)
      } else if (image === 'portrait' && this.portraitZoom < 5) {
        this.portraitZoom = Math.min(this.portraitZoom + 0.1, 5)
      }
    },
    zoomOut(image) {
      if (image === 'landscape' && this.landscapeZoom > 1) {
        this.landscapeZoom = Math.max(this.landscapeZoom - 0.1, 1)
      } else if (image === 'portrait' && this.portraitZoom > 1) {
        this.portraitZoom = Math.max(this.portraitZoom - 0.1, 1)
      }
    },
    async loadPoparan() {
      try {
        const response = await fetch('http://localhost:3000/api/poparan');
        const data = await response.json();
        this.poparanContent = data.content;
        this.editingPoparan = true;
        this.message = '';
      } catch (error) {
        console.error('Error loading poparan.txt:', error);
        this.message = 'Failed to load poparan.txt: ' + error.message;
      }
    },
    async savePoparan() {
      try {
        const response = await fetch('http://localhost:3000/api/poparan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: this.poparanContent })
        });
        const data = await response.json();
        this.message = data.message || 'Saved successfully';
      } catch (error) {
        console.error('Error saving poparan.txt:', error);
        this.message = 'Failed to save poparan.txt: ' + error.message;
      }
    },
    async generateFamilyTree() {
      this.loadingGenerate = true;
      this.message = '';
      try {
        const response = await fetch('http://localhost:3000/api/generate', {
          method: 'POST'
        });
        const data = await response.json();
        this.message = data.message || 'Generation complete';
        this.refreshImages();
      } catch (error) {
        console.error('Error generating family tree:', error);
        this.message = 'Failed to generate family tree: ' + error.message;
      } finally {
        this.loadingGenerate = false;
      }
    }
  },
  mounted() {
    this.loadFamilyTreeText();
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
.text-section, .image-section {
  flex: 1 1 45%;
  margin: 10px;
}
pre {
  white-space: pre-wrap;
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  max-height: 600px;
  overflow-y: auto;
  font-family: monospace;
}
.image-zoom-container {
  position: relative;
  display: inline-block;
  vertical-align: top;
  max-width: 100%;
}
img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: transform 0.3s ease;
  display: block;
}
.zoom-controls {
  margin-top: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  z-index: 10;
  background: white;
  padding: 4px 8px;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0,0,0,0.2);
  width: fit-content;
}
.zoom-controls button {
  padding: 4px 8px;
  font-size: 16px;
  cursor: pointer;
}
.zoom-controls span {
  font-weight: bold;
}
button {
  margin-top: 10px;
  padding: 6px 12px;
  font-size: 14px;
  cursor: pointer;
}
</style>
