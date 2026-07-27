/**
 * Mystical Journey (MJ) - Application Engine
 */

(function () {
  'use strict';

  // --- STATE ---
  let players = [];
  let activePlayerIndex = 0;
  let defaultDeck = [];
  let activeDeck = [];
  let drawnCards = [];
  let currentCard = null;
  let gameHistory = [];
  let selectedPlayerCount = 3;
  let leafletMap = null;

  // Preset Goal Suggestions
  const PRESET_GOALS = {
    energy: [
      "Harmonize relationships with my core team",
      "Cultivate deeper social presence & empathy",
      "Transform hidden interpersonal friction into energy"
    ],
    matter: [
      "Achieve tangible financial independence",
      "Structure physical environment and resources",
      "Manifest concrete material results for project"
    ],
    time: [
      "Master a complex field of knowledge",
      "Gain wisdom on optimal time allocation",
      "Synthesize information into actionable strategy"
    ]
  };

  // Guidance Prompts by Goal Type
  const GOAL_GUIDANCE = {
    energy: "⚡ Energy / Relations Focus: How does this text reflect your social connections, emotional alignment, or relationships?",
    matter: "💎 Matter / Money Focus: How does this text relate to your material goals, financial resources, or physical execution?",
    time: "⏳ Time / Information Focus: How does this text expand your knowledge, strategic perception, or time awareness?"
  };

  // --- INITIALIZATION ---
  document.addEventListener('DOMContentLoaded', async () => {
    await loadInitialCards();
    setupEventListeners();
    renderPlayerSetupForms(selectedPlayerCount);
  });

  // Load cards from cards.json
  async function loadInitialCards() {
    try {
      const resp = await fetch('cards.json');
      if (resp.ok) {
        defaultDeck = await resp.json();
      } else {
        throw new Error('Failed to fetch cards.json');
      }
    } catch (e) {
      console.warn('Fallback to basic cards generator', e);
      defaultDeck = generateFallbackDeck();
    }
    activeDeck = [...defaultDeck];
    shuffleArray(activeDeck);
  }

  function generateFallbackDeck() {
    const list = [];
    for (let i = 1; i <= 72; i++) {
      list.push({
        id: i,
        text: `Mystical Journey Card ${i}: Everything in the universe is a manifestation of time and energy.`
      });
    }
    return list;
  }

  // --- SETUP EVENT LISTENERS ---
  function setupEventListeners() {
    // Player count selector
    const countBtns = document.querySelectorAll('.count-btn');
    countBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        countBtns.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedPlayerCount = parseInt(btn.dataset.count, 10);
        renderPlayerSetupForms(selectedPlayerCount);
      });
    });

    // Aspect chip 3x3 picker listeners
    const aspectChips = document.querySelectorAll('.aspect-chip');
    const aspectBanner = document.getElementById('selected-aspect-banner');

    aspectChips.forEach(chip => {
      chip.addEventListener('click', () => {
        aspectChips.forEach(c => c.classList.remove('selected'));
        chip.classList.add('selected');
        const aspectVal = chip.dataset.aspect;
        if (aspectBanner) {
          aspectBanner.innerText = aspectVal;
        }
        if (currentCard) {
          currentCard.selectedAspect = aspectVal;
        }
      });
    });

    // UM Matrix Cell listeners
    const umCells = document.querySelectorAll('.um-cell');
    umCells.forEach(cell => {
      cell.addEventListener('click', () => {
        cell.classList.toggle('active');
      });
    });

    // Start game button
    document.getElementById('btn-start-game').addEventListener('click', startGame);

    // Header buttons
    document.getElementById('btn-metagame-info').addEventListener('click', () => openModal('modal-metagame'));
    document.getElementById('btn-restart').addEventListener('click', resetToSetup);
    document.getElementById('btn-history').addEventListener('click', () => openModal('modal-history'));
    document.getElementById('btn-deck-gallery').addEventListener('click', () => {
      renderDeckGallery();
      openModal('modal-deck');
    });
    document.getElementById('btn-map').addEventListener('click', () => {
      openModal('modal-map');
      setTimeout(initMapIfNeeded, 200);
    });

    // Gameplay buttons
    document.getElementById('btn-draw-card').addEventListener('click', drawCard);
    document.getElementById('btn-dispatch-coords').addEventListener('click', dispatchARGLocation);
    document.getElementById('card-stack-visual').addEventListener('click', drawCard);
    document.getElementById('btn-regen-deck').addEventListener('click', regenerateDeckFromBook);

    // Media upload handlers
    const uploadTrigger = document.getElementById('btn-upload-trigger');
    const mediaFileInput = document.getElementById('input-media-file');
    const mediaUrlInput = document.getElementById('input-media-url');
    const mediaPreviewImg = document.getElementById('media-preview-img');
    const mediaPreviewContainer = document.getElementById('media-preview-container');

    if (uploadTrigger && mediaFileInput) {
      uploadTrigger.addEventListener('click', () => mediaFileInput.click());
      mediaFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (evt) => {
            mediaPreviewImg.src = evt.target.result;
            mediaPreviewContainer.classList.remove('hidden');
          };
          reader.readAsDataURL(file);
        }
      });
    }

    if (mediaUrlInput) {
      mediaUrlInput.addEventListener('input', () => {
        const val = mediaUrlInput.value.trim();
        if (val) {
          mediaPreviewImg.src = val;
          mediaPreviewContainer.classList.remove('hidden');
        } else if (!mediaFileInput.files || !mediaFileInput.files.length) {
          mediaPreviewContainer.classList.add('hidden');
        }
      });
    }

    document.getElementById('btn-accept-card').addEventListener('click', () => handleInterpretation(true));
    document.getElementById('btn-defer-card').addEventListener('click', () => handleInterpretation(false));

    // Export buttons
    document.getElementById('btn-export-markdown').addEventListener('click', exportHistoryMarkdown);
    document.getElementById('btn-export-json').addEventListener('click', exportHistoryJSON);
    document.getElementById('btn-victory-export').addEventListener('click', exportHistoryMarkdown);
    document.getElementById('btn-victory-restart').addEventListener('click', () => {
      closeModal('modal-victory');
      resetToSetup();
    });

    // Modal Close buttons
    document.querySelectorAll('.modal-close').forEach(btn => {
      btn.addEventListener('click', () => {
        closeModal(btn.dataset.close);
      });
    });

    // Close modal on overlay click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal(overlay.id);
      });
    });

    // Map controls
    document.getElementById('btn-update-map').addEventListener('click', updateMapFromInputs);
    document.getElementById('btn-use-location').addEventListener('click', useBrowserLocation);
  }

  // --- RENDER PLAYER SETUP FORMS ---
  function renderPlayerSetupForms(count) {
    const container = document.getElementById('players-form-list');
    container.innerHTML = '';

    for (let i = 0; i < count; i++) {
      const pNum = i + 1;
      const defaultGoalType = i % 3 === 0 ? 'energy' : i % 3 === 1 ? 'matter' : 'time';
      
      const item = document.createElement('div');
      item.className = 'player-form-item';
      item.innerHTML = `
        <div class="player-form-header">
          <div class="player-title">🧙 Player ${pNum}</div>
        </div>
        
        <div class="form-group">
          <label class="form-label">Player Name</label>
          <input type="text" class="input-text p-name-input" value="Seeker ${pNum}" placeholder="Enter name">
        </div>

        <div class="form-group">
          <label class="form-label">Goal Category (Primary Triad)</label>
          <div class="goal-type-grid" data-pindex="${i}">
            <div class="goal-type-btn ${defaultGoalType === 'energy' ? 'selected' : ''}" data-type="energy">
              <span class="gt-name">⚡ Energy</span>
              <span class="gt-sub">Social / Relations</span>
            </div>
            <div class="goal-type-btn ${defaultGoalType === 'matter' ? 'selected' : ''}" data-type="matter">
              <span class="gt-name">💎 Matter</span>
              <span class="gt-sub">Material / Money</span>
            </div>
            <div class="goal-type-btn ${defaultGoalType === 'time' ? 'selected' : ''}" data-type="time">
              <span class="gt-name">⏳ Time</span>
              <span class="gt-sub">Knowledge / Info</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Stated Goal For This Journey</label>
          <input type="text" class="input-text p-goal-input" placeholder="State your specific goal..." value="${PRESET_GOALS[defaultGoalType][0]}">
          
          <div class="preset-goals" id="presets-container-${i}">
            ${renderPresetChips(defaultGoalType)}
          </div>
        </div>
      `;

      container.appendChild(item);

      // Attach event listeners for goal type selection per player
      const gtBtns = item.querySelectorAll('.goal-type-btn');
      const goalInput = item.querySelector('.p-goal-input');
      const presetsContainer = item.querySelector(`#presets-container-${i}`);

      gtBtns.forEach(gBtn => {
        gBtn.addEventListener('click', () => {
          gtBtns.forEach(b => b.classList.remove('selected'));
          gBtn.classList.add('selected');
          const type = gBtn.dataset.type;
          presetsContainer.innerHTML = renderPresetChips(type);
          goalInput.value = PRESET_GOALS[type][0];
          attachChipListeners(presetsContainer, goalInput);
        });
      });

      attachChipListeners(presetsContainer, goalInput);
    }
  }

  function renderPresetChips(type) {
    return PRESET_GOALS[type].map(text => 
      `<span class="preset-chip" data-text="${escapeHtml(text)}">${escapeHtml(text)}</span>`
    ).join('');
  }

  function attachChipListeners(container, inputElem) {
    container.querySelectorAll('.preset-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        inputElem.value = chip.dataset.text;
      });
    });
  }

  // --- START GAME ---
  function startGame() {
    players = [];
    const items = document.querySelectorAll('.player-form-item');
    
    items.forEach((item, idx) => {
      const name = item.querySelector('.p-name-input').value.trim() || `Player ${idx + 1}`;
      const selectedGtBtn = item.querySelector('.goal-type-btn.selected');
      const goalType = selectedGtBtn ? selectedGtBtn.dataset.type : 'energy';
      const goalText = item.querySelector('.p-goal-input').value.trim() || 'Transformative journey goal';

      // Team assignment: Even index = Team 1 (Clockwise), Odd index = Team 2 (Counter-CW)
      const team = (idx % 2 === 0) ? 1 : 2;
      const initialSphere = idx % 3; // 0: Info, 1: Matter, 2: Energy

      players.push({
        id: idx,
        name: name,
        team: team,
        spherePos: initialSphere,
        goalType: goalType,
        goalText: goalText,
        score: 0,
        collectedCards: []
      });
    });

    activePlayerIndex = 0;
    gameHistory = [];
    drawnCards = [];
    currentCard = null;

    if (activeDeck.length === 0) {
      activeDeck = [...defaultDeck];
      shuffleArray(activeDeck);
    }

    document.getElementById('view-setup').classList.add('hidden');
    document.getElementById('view-game').classList.remove('hidden');
    document.getElementById('btn-restart').classList.remove('hidden');

    renderScoreboard();
    renderSVGBoardTokens();
    resetArenaView();
    updateDeckCountUI();
  }

  // Render SVG Player Tokens on Triangle Vertices & Live HTML Position Bar
  function renderSVGBoardTokens() {
    const layer = document.getElementById('svg-player-tokens');
    const positionsBar = document.getElementById('player-sphere-positions-list');
    
    if (layer) layer.innerHTML = '';
    if (positionsBar) positionsBar.innerHTML = '';

    const coords = [
      { x: 220, y: 55, name: 'INFO' },     // 0: Information (Top)
      { x: 365, y: 310, name: 'MATTER' },  // 1: Matter (Bottom-Right)
      { x: 75, y: 310, name: 'ENERGY' }    // 2: Energy (Bottom-Left)
    ];

    const sphereNames = ['INFO Sphere', 'MATTER Sphere', 'ENERGY Sphere'];
    const colors = ['#f3c969', '#38bdf8', '#a855f7', '#f43f5e', '#10b981', '#f59e0b'];

    players.forEach((p, idx) => {
      const pos = coords[p.spherePos];
      const color = colors[idx % colors.length];
      const isActive = idx === activePlayerIndex;

      // Calculate radial offset so tokens orbit around the vertex circle
      const angle = (idx * (360 / Math.max(1, players.length))) * (Math.PI / 180);
      const orbitR = 36;
      const tokenX = pos.x + Math.cos(angle) * orbitR;
      const tokenY = pos.y + Math.sin(angle) * orbitR;

      if (layer) {
        // Active Pulse Ring
        if (isActive) {
          const pulse = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          pulse.setAttribute('cx', tokenX);
          pulse.setAttribute('cy', tokenY);
          pulse.setAttribute('r', '18');
          pulse.setAttribute('fill', 'none');
          pulse.setAttribute('stroke', color);
          pulse.setAttribute('stroke-width', '2');
          pulse.setAttribute('opacity', '0.6');
          layer.appendChild(pulse);
        }

        // Token Outer Glow Circle
        const tokenBg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        tokenBg.setAttribute('cx', tokenX);
        tokenBg.setAttribute('cy', tokenY);
        tokenBg.setAttribute('r', isActive ? '13' : '10');
        tokenBg.setAttribute('fill', color);
        tokenBg.setAttribute('stroke', isActive ? '#ffffff' : 'rgba(0,0,0,0.8)');
        tokenBg.setAttribute('stroke-width', isActive ? '3' : '1.5');
        layer.appendChild(tokenBg);

        // Player Initial Text inside Token
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', tokenX);
        text.setAttribute('y', tokenY + 4);
        text.setAttribute('fill', '#000000');
        text.setAttribute('font-size', '10');
        text.setAttribute('font-weight', 'bold');
        text.setAttribute('text-anchor', 'middle');
        text.textContent = `P${p.id + 1}`;
        layer.appendChild(text);

        // Player Name Label under token
        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', tokenX);
        label.setAttribute('y', tokenY + 22);
        label.setAttribute('fill', isActive ? '#f3c969' : '#ffffff');
        label.setAttribute('font-size', '9');
        label.setAttribute('font-weight', isActive ? 'bold' : 'normal');
        label.setAttribute('text-anchor', 'middle');
        label.textContent = p.name;
        layer.appendChild(label);
      }

      // Update HTML Live Positions Bar
      if (positionsBar) {
        const badge = document.createElement('div');
        badge.className = `player-pos-badge ${isActive ? 'active-p' : ''}`;
        badge.innerHTML = `
          <span style="width: 10px; height: 10px; border-radius: 50%; background: ${color}; display: inline-block;"></span>
          <strong>${escapeHtml(p.name)}</strong>
          <span style="color: var(--text-muted);">at</span>
          <span style="color: var(--accent-cyan); font-weight: 600;">${sphereNames[p.spherePos]}</span>
          ${isActive ? '<span style="color: var(--accent-gold); font-size: 0.7rem; font-weight: 800;">[TURN]</span>' : ''}
        `;
        positionsBar.appendChild(badge);
      }
    });
  }

  function resetToSetup() {
    document.getElementById('view-game').classList.add('hidden');
    document.getElementById('view-setup').classList.remove('hidden');
    document.getElementById('btn-restart').classList.add('hidden');
  }

  // --- RENDER SCOREBOARD ---
  function renderScoreboard() {
    const bar = document.getElementById('players-bar');
    bar.innerHTML = '';

    players.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = `player-status-card ${idx === activePlayerIndex ? 'active-turn' : ''}`;
      
      const dots = [0, 1, 2].map(dotIdx => 
        `<div class="score-dot ${dotIdx < p.score ? 'filled' : ''}"></div>`
      ).join('');

      card.innerHTML = `
        <div class="p-info">
          <span class="p-name">${escapeHtml(p.name)}</span>
          <span class="p-goal-tag ${p.goalType}">${p.goalType}</span>
        </div>
        <div class="p-goal-desc" title="${escapeHtml(p.goalText)}">🎯 ${escapeHtml(p.goalText)}</div>
        <div class="p-score">
          <span style="font-size: 0.75rem; color: var(--text-muted);">Insights:</span>
          <div class="score-dots">${dots}</div>
        </div>
      `;

      bar.appendChild(card);
    });
  }

  // --- DRAW CARD ---
  function drawCard() {
    if (activeDeck.length === 0) {
      alert("The deck is empty! Reshuffling drawn cards...");
      activeDeck = [...defaultDeck];
      shuffleArray(activeDeck);
    }

    currentCard = activeDeck.pop();
    drawnCards.push(currentCard);
    updateDeckCountUI();

    const activePlayer = players[activePlayerIndex];

    document.getElementById('arena-empty').classList.add('hidden');
    const activeArena = document.getElementById('arena-active');
    activeArena.classList.remove('hidden');

    document.getElementById('card-number-display').innerText = `Card ${currentCard.id}`;
    document.getElementById('card-text-display').innerText = `"${currentCard.text}"`;
    document.getElementById('card-goal-tag').innerText = `${activePlayer.goalType.toUpperCase()} GOAL`;
    document.getElementById('card-guidance-display').innerText = GOAL_GUIDANCE[activePlayer.goalType];

    document.getElementById('interp-player-label').innerText = activePlayer.name;
    document.getElementById('interpretation-text').value = '';

    // Initialize selected aspect banner
    const selectedAspectBtn = document.querySelector('.aspect-chip.selected');
    const aspectVal = selectedAspectBtn ? selectedAspectBtn.dataset.aspect : 'MATTER / MATTER';
    const aspectBanner = document.getElementById('selected-aspect-banner');
    if (aspectBanner) aspectBanner.innerText = aspectVal;
    if (currentCard) currentCard.selectedAspect = aspectVal;
  }

  function resetArenaView() {
    const activePlayer = players[activePlayerIndex];
    document.getElementById('active-player-name-placeholder').innerText = activePlayer.name;
    document.getElementById('arena-empty').classList.remove('hidden');
    document.getElementById('arena-active').classList.add('hidden');
    document.getElementById('arg-target-banner').classList.add('hidden');
    currentCard = null;
  }

  // --- DISPATCH ARG TARGET LOCATION ---
  function dispatchARGLocation() {
    if (!currentCard) {
      drawCard();
    }

    const latInput = parseFloat(document.getElementById('map-lat').value) || 51.5074;
    const lngInput = parseFloat(document.getElementById('map-lng').value) || -0.1278;
    const radiusKm = parseFloat(document.getElementById('map-radius').value) || 5;

    const sectorNum = Math.floor(Math.random() * 12) + 1;
    const randomAngle = (sectorNum - 1) * 30 + Math.random() * 30;
    const randomDistance = Math.random() * radiusKm;

    const targetCoords = offsetCoords(latInput, lngInput, randomDistance, randomAngle);
    const targetLat = targetCoords[0].toFixed(4);
    const targetLng = targetCoords[1].toFixed(4);

    setSupportLocationCard(targetLat, targetLng, `Sector ${sectorNum}`);

    alert(`📍 Support Location Assigned!\n\nTarget: ${targetLat}, ${targetLng}\nMystical Sector #${sectorNum}\n\nExplore this area to decode your card's secret message.`);
  }

  function updateDeckCountUI() {
    document.getElementById('deck-count-text').innerText = `${activeDeck.length} / 72 Cards Remaining`;
  }

  // --- INTERPRETATION HANDLER ---
  function handleInterpretation(accepted) {
    if (!currentCard) return;

    const activePlayer = players[activePlayerIndex];
    const interpText = document.getElementById('interpretation-text').value.trim();
    const debateSupport = document.getElementById('debate-support-text').value.trim();
    const debateOppose = document.getElementById('debate-oppose-text').value.trim();
    const mediaImgSrc = document.getElementById('media-preview-img').src || '';

    const selectedAspectBtn = document.querySelector('.aspect-chip.selected');
    const aspectTag = selectedAspectBtn ? selectedAspectBtn.dataset.aspect.toUpperCase() : 'MATTER / MATTER';

    // Active UM Matrix cells
    const activeUmCells = Array.from(document.querySelectorAll('.um-cell.active')).map(c => c.innerText);

    if (accepted && !interpText) {
      alert("Please enter your card interpretation before collecting the insight!");
      return;
    }

    // Move player token along the 3 spheres (0 -> 1 -> 2 -> 0)
    activePlayer.spherePos = (activePlayer.spherePos + 1) % 3;

    // Record turn in history
    const historyEntry = {
      round: gameHistory.length + 1,
      playerIndex: activePlayer.id,
      playerName: activePlayer.name,
      team: activePlayer.team,
      goalType: activePlayer.goalType,
      goalText: activePlayer.goalText,
      cardId: currentCard.id,
      cardText: currentCard.text,
      aspect: aspectTag,
      umCells: activeUmCells,
      interpretation: interpText || "(Deferred without interpretation)",
      debateSupport: debateSupport,
      debateOppose: debateOppose,
      mediaImg: mediaImgSrc,
      accepted: accepted,
      timestamp: new Date().toLocaleTimeString()
    };

    gameHistory.push(historyEntry);
    renderHistoryLog();

    // Reset fields
    document.querySelectorAll('.um-cell').forEach(c => c.classList.remove('active'));
    document.getElementById('interpretation-text').value = '';
    document.getElementById('debate-support-text').value = '';
    document.getElementById('debate-oppose-text').value = '';
    document.getElementById('input-media-url').value = '';
    document.getElementById('input-media-file').value = '';
    document.getElementById('media-preview-img').src = '';
    document.getElementById('media-preview-container').classList.add('hidden');

    if (accepted) {
      activePlayer.score += 1;
      activePlayer.collectedCards.push({
        card: currentCard,
        aspect: aspectTag,
        interpretation: interpText
      });

      renderScoreboard();
      renderSVGBoardTokens();

      // Check Win Condition: 3 cards collected
      if (activePlayer.score >= 3) {
        triggerVictory(activePlayer);
        return;
      }
    }

    // Rotate turn to next player
    activePlayerIndex = (activePlayerIndex + 1) % players.length;
    renderScoreboard();
    renderSVGBoardTokens();
    resetArenaView();
  }

  // --- DYNAMIC 72 CARD GENERATION FROM BOOK ---
  function regenerateDeckFromBook() {
    if (!window.MJ_BOOK_CHAPTERS || !window.MJ_BOOK_CHAPTERS.length) {
      alert("Book text unavailable for dynamic generation.");
      return;
    }

    if (!confirm("Generate a brand new set of 72 cards extracted live from the book? Current deck will be reset.")) {
      return;
    }

    const newCards = [];
    let cardId = 1;
    const chapters = window.MJ_BOOK_CHAPTERS;

    for (let cIdx = 0; cIdx < chapters.length && newCards.length < 72; cIdx++) {
      const chapterText = chapters[cIdx];
      const sentences = chapterText.match(/\b[A-Z][^.!?]*[.!?]/g) || [];
      
      let pickedInChapter = 0;
      while (pickedInChapter < 2 && sentences.length > 0 && newCards.length < 72) {
        const randIdx = Math.floor(Math.random() * sentences.length);
        const sentence = sentences.splice(randIdx, 1)[0].trim();
        
        if (sentence.split(/\s+/).length <= 200) {
          newCards.push({
            id: cardId++,
            text: sentence
          });
          pickedInChapter++;
        }
      }
    }

    // Fill up to 72 if needed
    while (newCards.length < 72) {
      newCards.push({
        id: cardId++,
        text: `Manifestation of Time and Space #${cardId}`
      });
    }

    activeDeck = newCards;
    shuffleArray(activeDeck);
    updateDeckCountUI();
    resetArenaView();
    alert("✨ Successfully generated 72 new cards from the book!");
  }

  // --- VICTORY MODAL ---
  function triggerVictory(winner) {
    document.getElementById('victory-winner-name').innerText = `👑 ${winner.name} Wins The Journey!`;
    document.getElementById('victory-winner-goal').innerText = `"${winner.goalText}" (${winner.goalType.toUpperCase()})`;

    const container = document.getElementById('victory-insights-list');
    container.innerHTML = winner.collectedCards.map((item, idx) => `
      <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid var(--accent-gold); border-radius: 8px; padding: 0.8rem;">
        <div style="font-family: var(--font-title); color: var(--accent-gold-light); font-weight: 700; margin-bottom: 0.3rem;">
          Insight #${idx + 1} - Card ${item.card.id}
        </div>
        <div style="font-style: italic; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">
          "${item.card.text}"
        </div>
        <div style="font-size: 0.9rem; color: #fff; background: rgba(0,0,0,0.3); padding: 0.5rem; border-radius: 4px;">
          💬 ${escapeHtml(item.interpretation)}
        </div>
      </div>
    `).join('');

    openModal('modal-victory');
  }

  // --- HISTORY & DECK GALLERY ---
  function renderHistoryLog() {
    const list = document.getElementById('history-list');
    if (gameHistory.length === 0) {
      list.innerHTML = '<p style="color: var(--text-muted); text-align: center;">No moves recorded yet.</p>';
      return;
    }

    list.innerHTML = gameHistory.map(entry => `
      <div class="history-item ${entry.accepted ? 'accepted' : ''}">
        <div class="history-meta">
          <span><strong>${escapeHtml(entry.playerName)}</strong> (Team ${entry.team || 1} • Turn ${entry.round})</span>
          <span>${entry.timestamp} • ${entry.accepted ? '⭐ INSIGHT COLLECTED' : '⏳ DEFERRED'}</span>
        </div>
        <div class="history-card-text">Card ${entry.cardId}: "${escapeHtml(entry.cardText)}"</div>
        <div style="font-size: 0.8rem; color: var(--accent-gold); font-weight: 700;">Aspect: ${escapeHtml(entry.aspect || 'MATTER / MATTER')}</div>
        ${entry.umCells && entry.umCells.length ? `<div style="font-size: 0.75rem; color: var(--accent-purple); margin-top: 0.2rem;">📐 <strong>UM Matrix Cypher:</strong> ${escapeHtml(entry.umCells.join(' | '))}</div>` : ''}
        ${entry.mediaImg ? `<div style="margin: 0.4rem 0;"><img src="${escapeHtml(entry.mediaImg)}" style="max-height: 100px; border-radius: 6px; border: 1px solid var(--accent-gold);"></div>` : ''}
        <div class="history-interpretation">💬 <strong>Interpretation:</strong> ${escapeHtml(entry.interpretation)}</div>
        ${entry.debateSupport ? `<div style="font-size: 0.8rem; color: #6ee7b7; background: rgba(16,185,129,0.1); padding: 0.4rem; border-radius: 4px; margin-top: 0.2rem;">↻ <strong>T1 Support:</strong> ${escapeHtml(entry.debateSupport)}</div>` : ''}
        ${entry.debateOppose ? `<div style="font-size: 0.8rem; color: #fda4af; background: rgba(244,63,94,0.1); padding: 0.4rem; border-radius: 4px; margin-top: 0.2rem;">↺ <strong>T2 Counter-Arg:</strong> ${escapeHtml(entry.debateOppose)}</div>` : ''}
      </div>
    `).join('');
  }

  function renderDeckGallery() {
    const grid = document.getElementById('deck-gallery-grid');
    grid.innerHTML = defaultDeck.map(card => `
      <div class="deck-gallery-card">
        <div class="num">Card ${card.id}</div>
        <div>"${escapeHtml(card.text)}"</div>
      </div>
    `).join('');
  }

  // Export Markdown Log
  function exportHistoryMarkdown() {
    if (gameHistory.length === 0) {
      alert("No history recorded to export yet.");
      return;
    }

    let md = `# Mystical Journey (MJ) - Session Log\n\n`;
    md += `**Date**: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}\n\n`;
    md += `## Players & Goals\n\n`;
    players.forEach(p => {
      md += `- **${p.name}** [${p.goalType.toUpperCase()}]: ${p.goalText} (Score: ${p.score}/3)\n`;
    });
    md += `\n## Turn Log\n\n`;

    gameHistory.forEach(h => {
      md += `### Turn ${h.round}: ${h.playerName}\n`;
      md += `- **Card**: #${h.cardId}\n`;
      md += `- **Quote**: "${h.cardText}"\n`;
      md += `- **Interpretation**: ${h.interpretation}\n`;
      md += `- **Status**: ${h.accepted ? 'Accepted (+1 Card)' : 'Deferred'}\n\n`;
    });

    downloadFile(md, 'mystical_journey_log.md', 'text/markdown');
  }

  // Export JSON Log
  function exportHistoryJSON() {
    const data = {
      date: new Date().toISOString(),
      players: players,
      history: gameHistory
    };
    downloadFile(JSON.stringify(data, null, 2), 'mystical_journey_log.json', 'application/json');
  }

  function downloadFile(content, fileName, contentType) {
    const a = document.createElement("a");
    const file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  // --- REAL-WORLD LEAFLET MAP ENGINE (12 Radial Sectors) ---
  function initMapIfNeeded() {
    if (leafletMap) return;

    const defaultLat = 51.5074;
    const defaultLng = -0.1278;
    const defaultRadiusKm = 5;

    leafletMap = L.map('map-element').setView([defaultLat, defaultLng], 11);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(leafletMap);

    // Map Click Listener to select custom area / coordinates as Support Location Card
    leafletMap.on('click', (e) => {
      const selectedLat = e.latlng.lat.toFixed(4);
      const selectedLng = e.latlng.lng.toFixed(4);

      document.getElementById('map-lat').value = selectedLat;
      document.getElementById('map-lng').value = selectedLng;

      setSupportLocationCard(selectedLat, selectedLng, "Custom Map Selection");
      alert(`📍 Custom Area Selected!\n\nCoordinates: ${selectedLat}, ${selectedLng}\nAssigned as your active card's Support Location Card.`);
    });

    renderRadialSectors(defaultLat, defaultLng, defaultRadiusKm);
  }

  function setSupportLocationCard(lat, lng, sectorLabel) {
    if (!currentCard) {
      drawCard();
    }

    const svLink = `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}`;
    const osmLink = `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lng}#map=16/${lat}/${lng}`;

    document.getElementById('arg-target-banner').classList.remove('hidden');
    document.getElementById('arg-coords-text').innerText = `${lat}, ${lng}`;
    document.getElementById('arg-sector-tag').innerText = sectorLabel || 'Selected Area';

    document.getElementById('link-google-streetview').href = svLink;
    document.getElementById('link-osm-map').href = osmLink;

    if (currentCard) {
      currentCard.supportLocation = { lat, lng, label: sectorLabel, svLink, osmLink };
    }

    if (leafletMap) {
      const pin = L.marker([parseFloat(lat), parseFloat(lng)]).addTo(leafletMap);
      pin.bindPopup(`📍 <strong>Support Location</strong><br>Coords: ${lat}, ${lng}<br><a href="${svLink}" target="_blank">Street View</a>`).openPopup();
    }
  }

  function updateMapFromInputs() {
    const lat = parseFloat(document.getElementById('map-lat').value) || 51.5074;
    const lng = parseFloat(document.getElementById('map-lng').value) || -0.1278;
    const radius = parseFloat(document.getElementById('map-radius').value) || 5;

    if (!leafletMap) initMapIfNeeded();
    leafletMap.setView([lat, lng], 12);
    renderRadialSectors(lat, lng, radius);
  }

  function useBrowserLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(pos => {
        document.getElementById('map-lat').value = pos.coords.latitude.toFixed(4);
        document.getElementById('map-lng').value = pos.coords.longitude.toFixed(4);
        updateMapFromInputs();
      }, () => {
        alert("Could not fetch location.");
      });
    } else {
      alert("Geolocation is not supported by your browser.");
    }
  }

  function renderRadialSectors(centerLat, centerLng, radiusKm) {
    if (!leafletMap) return;

    // Clear existing sector layers
    leafletMap.eachLayer(layer => {
      if (layer instanceof L.Polygon || layer instanceof L.Marker) {
        leafletMap.removeLayer(layer);
      }
    });

    const sections = 12;
    const angleStep = 360 / sections;

    for (let i = 0; i < sections; i++) {
      const startAngle = i * angleStep;
      const endAngle = (i + 1) * angleStep;
      const points = [[centerLat, centerLng]];

      const arcSamples = 6;
      const step = (endAngle - startAngle) / arcSamples;

      for (let s = 0; s <= arcSamples; s++) {
        const currAngle = startAngle + s * step;
        const pt = offsetCoords(centerLat, centerLng, radiusKm, currAngle);
        points.push(pt);
      }

      points.push([centerLat, centerLng]);

      const polygon = L.polygon(points, {
        color: '#e2b04c',
        weight: 2,
        fillColor: i % 2 === 0 ? '#38bdf8' : '#a855f7',
        fillOpacity: 0.25
      }).addTo(leafletMap);

      polygon.bindTooltip(`🔮 Mystical Sector ${i + 1} (${startAngle.toFixed(0)}° - ${endAngle.toFixed(0)}°)`, {
        permanent: false,
        direction: 'center'
      });
    }

    // Add Center Marker
    L.marker([centerLat, centerLng]).addTo(leafletMap)
      .bindPopup("🌟 Center of Mystical Journey Map").openPopup();
  }

  function offsetCoords(lat, lon, distanceKm, bearingDeg) {
    const R = 6371.0; // Earth radius in km
    const bearingRad = bearingDeg * Math.PI / 180;
    const latRad = lat * Math.PI / 180;
    const lonRad = lon * Math.PI / 180;
    const d = distanceKm / R;

    const newLatRad = Math.asin(
      Math.sin(latRad) * Math.cos(d) + Math.cos(latRad) * Math.sin(d) * Math.cos(bearingRad)
    );
    const newLonRad = lonRad + Math.atan2(
      Math.sin(bearingRad) * Math.sin(d) * Math.cos(latRad),
      Math.cos(d) - Math.sin(latRad) * Math.sin(newLatRad)
    );

    return [newLatRad * 180 / Math.PI, newLonRad * 180 / Math.PI];
  }

  // --- MODAL UTILS ---
  function openModal(id) {
    document.getElementById(id).classList.add('active');
  }

  function closeModal(id) {
    document.getElementById(id).classList.remove('active');
  }

  // --- UTILS ---
  function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, match => {
      const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
      return map[match];
    });
  }

})();
