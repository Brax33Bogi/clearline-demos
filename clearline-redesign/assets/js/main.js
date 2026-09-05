(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- mobile nav ---------------- */
  function initNav() {
    var header = document.querySelector("[data-header]");
    if (!header) return;
    var toggle = header.querySelector("[data-nav-toggle]");
    if (!toggle) return;
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.documentElement.style.overflow = open ? "hidden" : "";
    });
    header.querySelectorAll(".mobile-panel a").forEach(function (a) {
      a.addEventListener("click", function () {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        document.documentElement.style.overflow = "";
      });
    });
  }

  /* ---------------- capability explorer (tabs) ---------------- */
  function initExplorers() {
    document.querySelectorAll("[data-explorer]").forEach(function (root) {
      var tabs = Array.prototype.slice.call(root.querySelectorAll(".explorer-tab"));
      var panels = root.querySelectorAll(".explorer-panel");
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
          activate(tab.getAttribute("data-target"));
        });
        tab.addEventListener("keydown", function (e) {
          var idx = tabs.indexOf(tab);
          if (e.key === "ArrowRight") { e.preventDefault(); tabs[(idx + 1) % tabs.length].focus(); tabs[(idx + 1) % tabs.length].click(); }
          if (e.key === "ArrowLeft") { e.preventDefault(); tabs[(idx - 1 + tabs.length) % tabs.length].focus(); tabs[(idx - 1 + tabs.length) % tabs.length].click(); }
        });
      });
      function activate(target) {
        tabs.forEach(function (t) { t.setAttribute("aria-selected", t.getAttribute("data-target") === target ? "true" : "false"); });
        panels.forEach(function (p) {
          var match = p.id === "panel-" + target;
          p.classList.toggle("is-active", match);
          if (match) { p.hidden = false; } else { p.hidden = true; }
        });
      }
    });
  }

  /* ---------------- workspace demo ---------------- */
  function initWorkspaces() {
    document.querySelectorAll("[data-workspace]").forEach(function (ws) {
      var rows = ws.querySelectorAll(".ws-row");
      var detail = ws.querySelector("[data-ws-detail]");
      rows.forEach(function (row) {
        row.addEventListener("click", function () {
          rows.forEach(function (r) { r.classList.remove("is-selected"); r.setAttribute("aria-pressed", "false"); });
          row.classList.add("is-selected");
          row.setAttribute("aria-pressed", "true");
          renderDetail(row);
        });
      });

      function renderDetail(row) {
        if (!detail) return;
        var title = row.getAttribute("data-title");
        var meta = row.getAttribute("data-meta");
        var desc = row.getAttribute("data-desc");
        var status = row.getAttribute("data-status");
        var statusLabel = row.getAttribute("data-status-label");
        var history = JSON.parse(row.getAttribute("data-history") || "[]");
        var approvable = row.getAttribute("data-approvable") === "true";

        detail.querySelector("[data-f-title]").textContent = title;
        detail.querySelector("[data-f-meta]").textContent = meta;
        detail.querySelector("[data-f-desc]").textContent = desc;
        var tagEl = detail.querySelector("[data-f-status]");
        tagEl.textContent = statusLabel;
        tagEl.className = "row-tag " + (status === "ok" ? "tag-ok" : "tag-wait");

        var histEl = detail.querySelector("[data-f-history]");
        histEl.innerHTML = "";
        history.forEach(function (h) {
          var li = document.createElement("div");
          li.className = "ws-history-item";
          li.innerHTML = '<span class="hdot"></span><span>' + h + "</span>";
          histEl.appendChild(li);
        });

        var actionBtn = detail.querySelector("[data-ws-approve]");
        if (actionBtn) {
          actionBtn.disabled = !approvable;
          actionBtn.textContent = approvable ? "Approve & publish" : "Already live";
          actionBtn.onclick = approvable ? function () { approve(row, detail); } : null;
        }
      }

      function approve(row, detail) {
        row.setAttribute("data-status", "ok");
        row.setAttribute("data-status-label", "Live");
        row.setAttribute("data-approvable", "false");
        var hist = JSON.parse(row.getAttribute("data-history") || "[]");
        hist.push("Approved and published just now");
        row.setAttribute("data-history", JSON.stringify(hist));
        var rowTag = row.querySelector(".row-tag");
        if (rowTag) { rowTag.textContent = "Live"; rowTag.className = "row-tag tag-ok"; }
        renderDetail(row);
      }

      var firstSelected = ws.querySelector(".ws-row.is-selected") || rows[0];
      if (firstSelected) renderDetail(firstSelected);
    });
  }

  /* ---------------- AI receptionist demo ---------------- */
  function initChatDemos() {
    document.querySelectorAll("[data-chat-demo]").forEach(function (demo) {
      var playBtn = demo.querySelector("[data-chat-play]");
      var resetBtn = demo.querySelector("[data-chat-reset]");
      var bubbles = Array.prototype.slice.call(demo.querySelectorAll(".chat-bubble"));
      var fields = Array.prototype.slice.call(demo.querySelectorAll(".captured-field .val"));
      var handoff = demo.querySelector(".chat-handoff");
      var playing = false;

      function reset() {
        bubbles.forEach(function (b) { b.classList.remove("is-shown"); });
        fields.forEach(function (f) { f.classList.remove("is-filled"); });
        if (handoff) handoff.style.opacity = 0;
        playing = false;
        if (playBtn) { playBtn.disabled = false; playBtn.textContent = "Play the call"; }
      }

      function play() {
        if (playing) return;
        playing = true;
        reset();
        playing = true;
        if (playBtn) { playBtn.disabled = true; playBtn.textContent = "Playing…"; }
        if (reduceMotion) {
          bubbles.forEach(function (b) { b.classList.add("is-shown"); });
          fields.forEach(function (f) { f.classList.add("is-filled"); });
          if (handoff) handoff.style.opacity = 1;
          if (playBtn) { playBtn.disabled = false; playBtn.textContent = "Play again"; }
          playing = false;
          return;
        }
        var step = 0;
        function next() {
          if (step < bubbles.length) {
            bubbles[step].classList.add("is-shown");
            var fieldIdx = bubbles[step].getAttribute("data-reveals-field");
            if (fieldIdx !== null && fields[fieldIdx]) fields[fieldIdx].classList.add("is-filled");
            step++;
            setTimeout(next, 900);
          } else {
            if (handoff) { handoff.style.transition = "opacity 400ms ease"; handoff.style.opacity = 1; }
            if (playBtn) { playBtn.disabled = false; playBtn.textContent = "Play again"; }
            playing = false;
          }
        }
        setTimeout(next, 300);
      }

      if (playBtn) playBtn.addEventListener("click", play);
      if (resetBtn) resetBtn.addEventListener("click", reset);
      reset();
    });
  }

  /* ---------------- automation flow demo ---------------- */
  function initFlows() {
    document.querySelectorAll("[data-flow]").forEach(function (flow) {
      var stages = Array.prototype.slice.call(flow.querySelectorAll(".flow-stage"));
      var detail = flow.querySelector("[data-flow-detail]");
      stages.forEach(function (stage) {
        stage.addEventListener("click", function () { activate(stage); });
      });
      function activate(stage) {
        stages.forEach(function (s) { s.setAttribute("aria-pressed", s === stage ? "true" : "false"); });
        if (!detail) return;
        detail.querySelector("[data-fd-kicker]").textContent = stage.getAttribute("data-kicker");
        detail.querySelector("[data-fd-text]").textContent = stage.getAttribute("data-detail");
      }
      if (stages[0]) activate(stages[0]);
    });
  }

  /* ---------------- FAQ accordion ---------------- */
  function initFaqs() {
    document.querySelectorAll(".faq-item").forEach(function (item) {
      var q = item.querySelector(".faq-q");
      if (!q) return;
      q.addEventListener("click", function () {
        var open = item.getAttribute("data-open") === "true";
        item.closest(".faq").querySelectorAll(".faq-item").forEach(function (i) { i.setAttribute("data-open", "false"); i.querySelector(".faq-q").setAttribute("aria-expanded", "false"); });
        item.setAttribute("data-open", open ? "false" : "true");
        q.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
  }

  /* ---------------- start page: slots + form states ---------------- */
  function initStart() {
    var slots = document.querySelectorAll(".slot");
    slots.forEach(function (slot) {
      slot.addEventListener("click", function () {
        slots.forEach(function (s) { s.setAttribute("aria-pressed", "false"); });
        slot.setAttribute("aria-pressed", "true");
        var hidden = document.querySelector("[data-selected-slot]");
        if (hidden) hidden.value = slot.getAttribute("data-slot-label") || slot.textContent.trim();
      });
    });

    var form = document.querySelector("[data-start-form]");
    if (!form) return;
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var required = form.querySelectorAll("[required]");
      var missing = Array.prototype.slice.call(required).some(function (f) { return !f.value.trim(); });
      showStatus(missing ? "error" : "loading", missing ? "Add your name, business and best number so we know who is calling." : "Sending your request…");
      if (missing) return;
      setTimeout(function () {
        showStatus("success", "This is a design preview, so nothing was sent. Once this form is connected to Clearline's booking system, a real request lands in the portal and you get a text to confirm.");
      }, 900);
    });
    function showStatus(kind, text) {
      status.className = "form-status is-visible is-" + kind;
      status.textContent = text;
      status.setAttribute("role", kind === "error" ? "alert" : "status");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initExplorers();
    initWorkspaces();
    initChatDemos();
    initFlows();
    initFaqs();
    initStart();
  });
})();
