// AI Animations and Interactions
class AIAnimations {
    constructor() {
        this.init();
    }

    init() {
        this.setupAIProcessingAnimations();
        this.setupTypingAnimations();
        this.setupHoverAnimations();
        this.setupScrollAnimations();
        this.setupLoadingAnimations();
    }

    // AI Processing Animations
    setupAIProcessingAnimations() {
        // Add AI processing animation to all AI-related buttons
        const aiButtons = document.querySelectorAll('.btn-ai, [data-ai-action]');
        aiButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.showAIProcessing(button);
            });
        });

        // Add AI thinking animation to inputs
        const aiInputs = document.querySelectorAll('input[placeholder*="AI"], input[placeholder*="learn"], input[placeholder*="course"]');
        aiInputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.classList.add('ai-thinking');
            });
            
            input.addEventListener('blur', () => {
                input.classList.remove('ai-thinking');
            });
        });
    }

    showAIProcessing(element) {
        const originalText = element.innerHTML;
        const originalClasses = element.className;
        
        // Add processing animation
        element.classList.add('ai-processing');
        element.innerHTML = '<i class="fas fa-cog fa-spin"></i> AI is processing...';
        element.disabled = true;

        // Simulate AI processing time
        setTimeout(() => {
            element.classList.remove('ai-processing');
            element.innerHTML = originalText;
            element.disabled = false;
            element.classList.add('animate-bounce');
            
            setTimeout(() => {
                element.classList.remove('animate-bounce');
            }, 1000);
        }, 2000);
    }

    // Typing Animations
    setupTypingAnimations() {
        const typingElements = document.querySelectorAll('.text-typing');
        typingElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            element.style.width = '0';
            
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    element.style.width = ((i + 1) / text.length * 100) + '%';
                    i++;
                    setTimeout(typeWriter, 100);
                }
            };
            
            // Start typing animation when element is visible
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        typeWriter();
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(element);
        });
    }

    // Hover Animations
    setupHoverAnimations() {
        // Add hover animations to cards
        const cards = document.querySelectorAll('.card-animate, .qa-card, .feature-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.classList.add('hover-lift');
            });
            
            card.addEventListener('mouseleave', () => {
                card.classList.remove('hover-lift');
            });
        });

        // Add glow effect to AI elements
        const aiElements = document.querySelectorAll('[data-ai-element]');
        aiElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.classList.add('hover-glow');
            });
            
            element.addEventListener('mouseleave', () => {
                element.classList.remove('hover-glow');
            });
        });
    }

    // Scroll Animations
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Add staggered animation to children
                    const children = entry.target.querySelectorAll('.stagger-animate');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('animate-fade-in');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        // Observe all elements with animate-on-scroll class
        const scrollElements = document.querySelectorAll('.animate-on-scroll');
        scrollElements.forEach(element => {
            observer.observe(element);
        });
    }

    // Loading Animations
    setupLoadingAnimations() {
        // Show loading animation for AI operations
        this.showAILoading = (container) => {
            const loadingHTML = `
                <div class="ai-loading-overlay">
                    <div class="loading-spinner"></div>
                    <p class="ai-loading-text">AI is thinking...</p>
                </div>
            `;
            
            container.innerHTML = loadingHTML;
            container.classList.add('ai-loading');
        };

        // Hide loading animation
        this.hideAILoading = (container, content) => {
            container.classList.remove('ai-loading');
            container.innerHTML = content;
        };
    }

    // AI Status Indicators
    showAIStatus(status, element) {
        const statusClasses = {
            'processing': 'ai-status processing',
            'success': 'ai-status',
            'error': 'ai-status error'
        };

        element.className = statusClasses[status] || 'ai-status';
        
        setTimeout(() => {
            element.classList.remove('processing', 'error');
        }, 3000);
    }

    // Animate AI Response
    animateAIResponse(element, response) {
        element.classList.add('ai-generating');
        element.textContent = '';
        
        let i = 0;
        const typeResponse = () => {
            if (i < response.length) {
                element.textContent += response.charAt(i);
                i++;
                setTimeout(typeResponse, 50);
            } else {
                element.classList.remove('ai-generating');
            }
        };
        
        typeResponse();
    }

    // Floating Animation for AI Elements
    addFloatingAnimation() {
        const floatingElements = document.querySelectorAll('.ai-float');
        floatingElements.forEach(element => {
            element.classList.add('animate-float');
        });
    }

    // Pulse Animation for Important Elements
    addPulseAnimation() {
        const pulseElements = document.querySelectorAll('.ai-pulse');
        pulseElements.forEach(element => {
            element.classList.add('animate-pulse');
        });
    }

    // Shimmer Effect for Loading States
    addShimmerEffect(element) {
        element.classList.add('animate-shimmer');
        
        setTimeout(() => {
            element.classList.remove('animate-shimmer');
        }, 2000);
    }
}

// Initialize AI Animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiAnimations = new AIAnimations();
    
    // Add AI-specific classes to elements
    const aiButtons = document.querySelectorAll('button[onclick*="generate"], button[onclick*="create"]');
    aiButtons.forEach(button => {
        button.classList.add('btn-ai');
    });
    
    // Add AI status indicators
    const aiElements = document.querySelectorAll('.ai-element');
    aiElements.forEach(element => {
        element.classList.add('ai-status');
    });
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIAnimations;
} 