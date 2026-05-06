// Page navigation
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Update active button
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update active page
        const pageName = btn.dataset.page;
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.getElementById(`${pageName}-page`).classList.add('active');

        // Load data for the page
        if (pageName === 'campaigns') {
            loadCampaigns();
        } else if (pageName === 'settings') {
            loadConfig();
        }
    });
});

// Modal management
const campaignModal = document.getElementById('campaign-modal');
const campaignForm = document.getElementById('campaign-form');
const addCampaignBtn = document.getElementById('add-campaign-btn');
const modalCloseBtn = document.querySelector('.modal-close');
const modalCancelBtn = document.getElementById('modal-cancel');

addCampaignBtn.addEventListener('click', () => {
    document.getElementById('modal-title').textContent = 'Add Campaign';
    campaignForm.reset();
    document.getElementById('campaign-id').value = '';
    document.getElementById('post-preview').classList.add('hidden');
    campaignModal.classList.add('active');
});

modalCloseBtn.addEventListener('click', () => {
    campaignModal.classList.remove('active');
});

modalCancelBtn.addEventListener('click', () => {
    campaignModal.classList.remove('active');
});

// Close modal on background click
campaignModal.addEventListener('click', (e) => {
    if (e.target === campaignModal) {
        campaignModal.classList.remove('active');
    }
});

// Post ID blur event - fetch post details
document.getElementById('post-id').addEventListener('blur', async (e) => {
    const postId = e.target.value.trim();
    if (!postId) return;

    try {
        const config = await fetch('/api/config').then(r => r.json());
        if (!config) {
            alert('Please configure Instagram credentials first');
            return;
        }

        const response = await fetch(`/api/campaigns/${postId}`).catch(() => null);
        // Note: In a real implementation, you'd call the Instagram API to fetch post details
        // For now, we'll just show the post ID in the preview

        document.getElementById('post-preview').classList.remove('hidden');
        document.getElementById('post-image').src = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22200%22%3E%3Crect fill=%22%23252d35%22 width=%22400%22 height=%22200%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-size=%2216%22 fill=%22%2365676b%22%3EPost ID: ' + postId + '%3C/text%3E%3C/svg%3E';
        document.getElementById('post-caption').textContent = `Loaded post: ${postId}`;
    } catch (error) {
        console.error('Error loading post details:', error);
    }
});

// Campaign form submission
campaignForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const campaignId = document.getElementById('campaign-id').value;
    const postId = document.getElementById('post-id').value;
    const keywords = document.getElementById('keywords').value;
    const commentReply = document.getElementById('comment-reply').value;
    const dmMessage = document.getElementById('dm-message').value;

    if (!postId || !keywords || !commentReply || !dmMessage) {
        alert('Please fill in all required fields');
        return;
    }

    const data = {
        post_id: postId,
        keywords,
        comment_reply: commentReply,
        dm_message: dmMessage,
    };

    try {
        let response;
        if (campaignId) {
            // Update existing campaign
            response = await fetch(`/api/campaigns/${campaignId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
        } else {
            // Create new campaign
            response = await fetch('/api/campaigns', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
        }

        if (response.ok) {
            campaignModal.classList.remove('active');
            loadCampaigns();
            alert('Campaign saved successfully!');
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail || 'Failed to save campaign'}`);
        }
    } catch (error) {
        console.error('Error saving campaign:', error);
        alert('Error saving campaign');
    }
});

// Load campaigns
async function loadCampaigns() {
    try {
        const response = await fetch('/api/campaigns');
        const campaigns = await response.json();

        const campaignsList = document.getElementById('campaigns-list');

        if (!campaigns || campaigns.length === 0) {
            campaignsList.innerHTML = '<div class="loading">No campaigns yet. Click "Add Campaign" to create one.</div>';
            return;
        }

        campaignsList.innerHTML = campaigns.map(campaign => `
            <div class="campaign-card">
                <div class="campaign-header">
                    <span class="campaign-title">Post ${campaign.post_id.slice(-8)}</span>
                    <span class="campaign-status ${campaign.active ? 'active' : 'inactive'}">
                        ${campaign.active ? 'Active' : 'Inactive'}
                    </span>
                </div>

                <div class="campaign-field">
                    <div class="campaign-field-label">Keywords</div>
                    <div class="campaign-field-value">${campaign.keywords}</div>
                </div>

                <div class="campaign-field">
                    <div class="campaign-field-label">Comment Reply</div>
                    <div class="campaign-field-value" style="white-space: pre-wrap;">${campaign.comment_reply}</div>
                </div>

                <div class="campaign-field">
                    <div class="campaign-field-label">DM Message</div>
                    <div class="campaign-field-value" style="white-space: pre-wrap;">${campaign.dm_message}</div>
                </div>

                <div class="campaign-actions">
                    <button class="btn btn-secondary btn-small" onclick="editCampaign(${campaign.id})">Edit</button>
                    <button class="btn btn-secondary btn-small" onclick="toggleCampaign(${campaign.id})">
                        ${campaign.active ? 'Pause' : 'Resume'}
                    </button>
                    <button class="btn btn-danger btn-small" onclick="deleteCampaign(${campaign.id})">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading campaigns:', error);
        document.getElementById('campaigns-list').innerHTML = '<div class="loading">Error loading campaigns</div>';
    }
}

// Edit campaign
async function editCampaign(id) {
    try {
        const response = await fetch(`/api/campaigns/${id}`);
        const campaign = await response.json();

        document.getElementById('modal-title').textContent = 'Edit Campaign';
        document.getElementById('campaign-id').value = campaign.id;
        document.getElementById('post-id').value = campaign.post_id;
        document.getElementById('keywords').value = campaign.keywords;
        document.getElementById('comment-reply').value = campaign.comment_reply;
        document.getElementById('dm-message').value = campaign.dm_message;

        // Show post preview
        if (campaign.post_media_url) {
            document.getElementById('post-preview').classList.remove('hidden');
            document.getElementById('post-image').src = campaign.post_media_url;
            document.getElementById('post-caption').textContent = campaign.post_caption || 'No caption';
        }

        campaignModal.classList.add('active');
    } catch (error) {
        console.error('Error loading campaign:', error);
        alert('Error loading campaign');
    }
}

// Toggle campaign active status
async function toggleCampaign(id) {
    try {
        await fetch(`/api/campaigns/${id}/toggle`, { method: 'POST' });
        loadCampaigns();
    } catch (error) {
        console.error('Error toggling campaign:', error);
        alert('Error toggling campaign');
    }
}

// Delete campaign
async function deleteCampaign(id) {
    if (!confirm('Are you sure you want to delete this campaign?')) return;

    try {
        const response = await fetch(`/api/campaigns/${id}`, { method: 'DELETE' });
        if (response.ok) {
            loadCampaigns();
        } else {
            alert('Error deleting campaign');
        }
    } catch (error) {
        console.error('Error deleting campaign:', error);
        alert('Error deleting campaign');
    }
}

// Settings form
const configForm = document.getElementById('config-form');

configForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        instagram_access_token: document.getElementById('access-token').value,
        instagram_business_account_id: document.getElementById('business-account-id').value,
        facebook_page_id: document.getElementById('page-id').value || null,
    };

    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const status = document.getElementById('config-status');
        if (response.ok) {
            status.classList.remove('hidden', 'error');
            status.classList.add('success');
            status.textContent = 'Configuration saved successfully!';
        } else {
            status.classList.remove('hidden', 'success');
            status.classList.add('error');
            status.textContent = 'Error saving configuration';
        }
    } catch (error) {
        console.error('Error saving config:', error);
        const status = document.getElementById('config-status');
        status.classList.remove('hidden', 'success');
        status.classList.add('error');
        status.textContent = 'Error saving configuration';
    }
});

// Load config
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();

        if (config) {
            document.getElementById('business-account-id').value = config.instagram_business_account_id || '';
            document.getElementById('page-id').value = config.facebook_page_id || '';
        }
    } catch (error) {
        console.error('Error loading config:', error);
    }
}

// Setup guide function
function showSetupGuide() {
    const settingsPage = document.getElementById('settings-page');
    settingsPage.scrollIntoView({ behavior: 'smooth' });
}

// Set webhook URL in setup guide
document.addEventListener('DOMContentLoaded', () => {
    const webhookUrl = `${window.location.origin}/webhook/instagram`;
    const webhookElement = document.getElementById('webhook-url');
    if (webhookElement) {
        webhookElement.textContent = webhookUrl;
    }

    // Load campaigns on page load
    loadCampaigns();
});
