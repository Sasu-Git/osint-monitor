/* Situational-awareness workspace: the MapLibre map and its synchronisation with the HTMX feed.

   One source of truth: the filter form (#ws-filters). The feed is swapped by HTMX from it; the map reads the
   same form to fetch /api/workspace/developments.geojson. Clicking a country sets the form's country field,
   clicking a marker opens its preview in the context rail, and every feed swap reloads the map.
   No state is kept here beyond the map view itself. */
(function () {
  "use strict";

  const LEVEL_COLOR = ["match", ["get", "level"], "HIGH", "#f0b44c", "LOW", "#5d6875", "MUTED", "#3a424d", "#8fb3d9"];
  const LEVEL_RADIUS = ["match", ["get", "level"], "HIGH", 7.5, "LOW", 4.5, "MUTED", 4, 5.5];
  const GLYPHS = "https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf";

  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c])); }
  function form() { return document.getElementById("ws-filters"); }

  function geojsonUrl(el) {
    const base = el.dataset.geojson;
    const f = form();
    if (!f) return base;
    const params = new URLSearchParams(new FormData(f));
    return base + (base.includes("?") ? "&" : "?") + params.toString();
  }

  function when(iso) {
    if (!iso) return "time unknown";
    const d = new Date(iso + (iso.endsWith("Z") ? "" : "Z"));
    return d.toLocaleString(undefined, {day: "numeric", month: "short", hour: "2-digit", minute: "2-digit", timeZone: "UTC"}) + " UTC";
  }

  function tooltip(p) {
    const actors = (typeof p.actors === "string" ? JSON.parse(p.actors) : p.actors) || [];
    return `<div class="tip"><b>${esc(p.title)}</b>
      <div class="tip-line">${esc(when(p.time))}${p.place ? " · " + esc(p.place) + (p.country_level ? " (whole country)" : "") : ""}</div>
      <div class="tip-line">${actors.length ? esc(actors.join(" · ")) : "<i>No principal actors identified</i>"}</div>
      <div class="tip-line">${p.situation ? "Part of <b>" + esc(p.situation) + "</b>" : "<i>No active situation</i>"}</div>
      <div class="tip-line">${esc(p.sources)} independent source${p.sources == 1 ? "" : "s"}</div></div>`;
  }

  function initMap(el) {
    if (!window.maplibregl) { el.innerHTML = '<p class="hint map-fallback">Map library unavailable; the feed lists every development.</p>'; return; }
    const workspace = el.dataset.mode === "workspace";
    const map = new maplibregl.Map({
      container: el, attributionControl: false, dragRotate: false, pitchWithRotate: false,
      center: [20, 25], zoom: 1.3, minZoom: 0.8, maxZoom: 9, renderWorldCopies: false,
      style: {
        version: 8, glyphs: GLYPHS,
        sources: {
          countries: {type: "geojson", data: "/static/geo/countries.geojson", promoteId: "id"},
          devs: {type: "geojson", data: geojsonUrl(el), cluster: true, clusterRadius: 36, clusterMaxZoom: 5,
                 clusterProperties: {high: ["+", ["case", ["==", ["get", "level"], "HIGH"], 1, 0]]}},
        },
        layers: [
          {id: "bg", type: "background", paint: {"background-color": css("--map-sea") || "#0b0f14"}},
          {id: "land", type: "fill", source: "countries", paint: {
            "fill-color": ["case", ["boolean", ["feature-state", "selected"], false], css("--map-selected") || "#20344c",
                           ["boolean", ["feature-state", "hover"], false], css("--map-hover") || "#1c2530", css("--map-land") || "#161d26"]}},
          {id: "borders", type: "line", source: "countries", paint: {"line-color": css("--map-border") || "#2a3442", "line-width": 0.6}},
          {id: "clusters", type: "circle", source: "devs", filter: ["has", "point_count"], paint: {
            "circle-color": "#3b5470",
            "circle-stroke-color": ["case", [">", ["get", "high"], 0], "#f0b44c", "#8fb3d9"],
            "circle-stroke-width": ["case", [">", ["get", "high"], 0], 2.5, 1],
            "circle-radius": ["step", ["get", "point_count"], 11, 10, 15, 40, 20]}},
          {id: "cluster-count", type: "symbol", source: "devs", filter: ["has", "point_count"], layout: {
            "text-field": ["get", "point_count_abbreviated"], "text-font": ["Open Sans Semibold"], "text-size": 11},
            paint: {"text-color": "#e6e9ee"}},
          {id: "points", type: "circle", source: "devs", filter: ["!", ["has", "point_count"]], paint: {
            "circle-color": ["case", ["get", "country_level"], "rgba(0,0,0,0)", LEVEL_COLOR],
            "circle-stroke-color": LEVEL_COLOR, "circle-stroke-width": ["case", ["get", "country_level"], 2, 1],
            "circle-radius": LEVEL_RADIUS, "circle-opacity": 0.95}},
          {id: "highlight", type: "circle", source: "devs", filter: ["==", ["get", "id"], -1], paint: {
            "circle-color": "rgba(0,0,0,0)", "circle-stroke-color": "#ffffff", "circle-stroke-width": 2, "circle-radius": 11}},
        ],
      },
    });
    map.addControl(new maplibregl.NavigationControl({showCompass: false}), "top-right");
    map.addControl(new maplibregl.AttributionControl({compact: true, customAttribution: "Boundaries: Natural Earth"}));
    el._map = map;
    const popup = new maplibregl.Popup({closeButton: false, closeOnClick: false, maxWidth: "320px", offset: 10});
    let hovered = null, selected = null;

    function selectCountry(id) {
      if (selected) map.setFeatureState({source: "countries", id: selected}, {selected: false});
      selected = id || null;
      if (selected) map.setFeatureState({source: "countries", id: selected}, {selected: true});
    }

    map.on("load", () => {
      const f = form();
      if (f && f.country && f.country.value) selectCountry(f.country.value);
      if (!workspace) fitToData(map, geojsonUrl(el));
    });

    map.on("mouseenter", "points", e => {
      map.getCanvas().style.cursor = "pointer";
      const ft = e.features[0];
      popup.setLngLat(ft.geometry.coordinates).setHTML(tooltip(ft.properties)).addTo(map);
    });
    map.on("mouseleave", "points", () => { map.getCanvas().style.cursor = ""; popup.remove(); });
    map.on("mouseenter", "clusters", () => { map.getCanvas().style.cursor = "pointer"; });
    map.on("mouseleave", "clusters", () => { map.getCanvas().style.cursor = ""; });

    map.on("click", "clusters", e => {
      const ft = map.queryRenderedFeatures(e.point, {layers: ["clusters"]})[0];
      map.getSource("devs").getClusterExpansionZoom(ft.properties.cluster_id).then(zoom => {
        map.easeTo({center: ft.geometry.coordinates, zoom: Math.min(zoom + 0.2, 9)});
      });
    });

    map.on("click", "points", e => {
      const id = e.features[0].properties.id;
      if (!workspace) { window.location.href = "/developments/" + id; return; }
      showPreview(id);
      highlight(id);
    });

    if (workspace) {
      map.on("mousemove", "land", e => {
        const id = e.features[0] && e.features[0].id;
        if (hovered && hovered !== id) map.setFeatureState({source: "countries", id: hovered}, {hover: false});
        hovered = id;
        if (id) map.setFeatureState({source: "countries", id}, {hover: true});
      });
      map.on("mouseleave", "land", () => {
        if (hovered) map.setFeatureState({source: "countries", id: hovered}, {hover: false});
        hovered = null;
      });
      map.on("click", e => {
        if (map.queryRenderedFeatures(e.point, {layers: ["points", "clusters"]}).length) return;
        const land = map.queryRenderedFeatures(e.point, {layers: ["land"]})[0];
        const id = land ? land.id : "";
        const f = form();
        if (!f) return;
        const next = f.country.value === id ? "" : id;          // clicking the selected country clears it
        setCountry(next, land && next ? land.properties.name : "");
        selectCountry(next);
      });
    }
    return map;
  }

  function fitToData(map, url) {
    fetch(url).then(r => r.ok ? r.json() : null).then(j => {
      if (!j || !j.features || !j.features.length) return;
      const b = new maplibregl.LngLatBounds();
      j.features.forEach(ft => b.extend(ft.geometry.coordinates));
      map.fitBounds(b, {padding: 40, maxZoom: 5, duration: 0});
    }).catch(() => {});
  }

  function highlight(id) {
    const el = document.getElementById("map");
    if (el && el._map && el._map.getLayer("highlight")) el._map.setFilter("highlight", ["==", ["get", "id"], id == null ? -1 : Number(id)]);
  }

  function showPreview(id) {
    const target = document.getElementById("preview");
    if (!target || !window.htmx) { window.location.href = "/developments/" + id; return; }
    htmx.ajax("GET", "/developments/" + id + "/preview", {target: "#preview", swap: "innerHTML"});
    document.body.classList.add("open-rail-right");
  }

  function setCountry(id, name) {
    const f = form();
    if (!f) return;
    f.country.value = id || "";
    const box = document.getElementById("country-filter");
    if (box) { box.hidden = !id; document.getElementById("country-filter-name").textContent = name || id || ""; }
    if (window.htmx) htmx.trigger(f, "change"); else f.submit();
  }

  function reloadMap() {
    const el = document.getElementById("map");
    if (!el || !el._map) return;
    const src = el._map.getSource("devs");
    if (src) src.setData(geojsonUrl(el));
  }

  document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("map");
    if (el) initMap(el);

    // feed swapped (filters or priorities changed): reload the map from the same form
    document.body.addEventListener("htmx:afterSettle", e => { if (e.detail.target && e.detail.target.id === "feed") reloadMap(); });

    // feed card hover highlights its marker; situation hover in the rail highlights that Situation's markers
    document.body.addEventListener("mouseover", e => {
      const card = e.target.closest && e.target.closest(".dev[data-id]");
      if (card) { highlight(card.dataset.id); return; }
      const sit = e.target.closest && e.target.closest("[data-situation]");
      const m = document.getElementById("map");
      if (sit && sit.dataset.situation && m && m._map && m._map.getLayer("highlight"))
        m._map.setFilter("highlight", ["==", ["get", "situation_slug"], sit.dataset.situation]);
    });

    document.body.addEventListener("click", e => {
      const t = e.target.closest("[data-toggle]");
      if (t) {
        const id = t.dataset.toggle;
        document.body.classList.toggle("open-" + id);
        document.body.classList.toggle("collapsed-" + id);
        const m = document.getElementById("map");
        if (m && m._map) setTimeout(() => m._map.resize(), 220);
        return;
      }
      if (e.target.closest("[data-clear-country]")) {
        setCountry("", "");
        const m = document.getElementById("map");
        if (m && m._map) m._map.removeFeatureState({source: "countries"});
      }
    });

  });
})();
