
    window.onload = function() {
        const urlParams = new URLSearchParams(window.location.search);
        const tag = urlParams.get('tag');
        
        if (tag) {
            // Hide all operations initially
            document.querySelectorAll('.opblock-tag-section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Show only the selected tag
            const tagSection = document.querySelector(`.opblock-tag[data-tag="${tag}"]`);
            if (tagSection) {
                tagSection.closest('.opblock-tag-section').style.display = 'block';
            }
            
            // Update UI to reflect selection
            const filterInput = document.querySelector('.opblock-tag-filter input');
            if (filterInput) {
                filterInput.value = tag;
                filterInput.dispatchEvent(new Event('input'));
            }
        }
        
        // Add tag links to the header
        const header = document.querySelector('.swagger-ui .topbar');
        if (header) {
            const tags = Array.from(document.querySelectorAll('.opblock-tag')).map(t => t.getAttribute('data-tag'));
            
            tags.forEach(tag => {
                const link = document.createElement('a');
                link.href = `?tag=${tag}`;
                link.textContent = tag;
                link.style.margin = '0 10px';
                link.style.color = '#ffffff';
                header.appendChild(link);
            });
        }
    }
    