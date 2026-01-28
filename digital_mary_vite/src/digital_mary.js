// css
import './assets/digital_mary.scss'

// libs
import './jquery_load_fix.js'
import select2 from 'select2'
select2()
import 'jquery-ui-dist/jquery-ui.js'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'glider-js/glider.min.js'
import { Popover } from 'bootstrap'
import Viewer from 'viewerjs'

/* Basic scripts for the Digital Mary Project
 */

import Accordion from 'dhilux/js/accordion.js';
import LazyLoad from 'dhilux/js/lazyload.js';
/* First thing to do is set up the images for the viewer thing */

(() => {
    let gallery
    let glider
    let imgSlider = document.querySelector('.image-slider');
    let dmViewerContainer = document.querySelector('#dm-viewer-container');

    init();

    function init(){
        // First add the JS class
        document.querySelector('body').classList.add('js');
        /* Add special viewer stuff */
        if (dmViewerContainer && imgSlider){
            makeGlider();
            makeImageTools();
            makeImageViewer();
        }
        enhanceLazyLoad();
        makeHamburgers();
        makeAccordions();
        cleanupText();

        document.querySelectorAll('[data-bs-toggle="popover"]').forEach((popoverTriggerEl) => {
            return new Popover(popoverTriggerEl, {
                html: true,
                // trigger: 'focus',
            })
        })
        document.querySelectorAll('.django-select2').forEach((djangoSelect2El) => {
            $(djangoSelect2El).select2()
        })
    }

    function makeHamburgers(){
        document.querySelectorAll('.hamburger').forEach(ham => {
            ham.addEventListener('click', e => {
                ham.classList.toggle('is-active');
            })
        });
    }

    function makeAccordions(){
    // Now make details
        document.querySelectorAll('details').forEach(el => {
            let accordion = new Accordion(el);
        });
    }

    function cleanupText(){
    // Hacks for fixing up the descriptions
    // Clean up some descriptions, but this is a hack
        let nbspRex = /^\s*&nbsp;\s*$/
        document.querySelectorAll('.item-description').forEach(div => {
            div.querySelectorAll('p').forEach(p => {
                let text = p.innerHTML;
                if (nbspRex.test(text)){
                    p.parentElement.removeChild(p);
                }
            })
        });

    }

    function makeGlider(){
        let imgSection = document.querySelector('.images');
        let imgCtr = imgSection.querySelector('div');
        let slides = imgSlider.querySelectorAll('.item');

        if (slides.length > 1) {
            imgSlider.addEventListener('glider-loaded', e => {
                imgCtr.classList.add('loaded');
            });
            // Set up a new glider
            glider = new Glider(imgSlider, {
                scrollLock: true,
                dots: '.dots',
                arrows: {
                    prev: '.slider-btn-prev',
                    next: '.slider-btn-next'
                },
                duration: 1
            })

        }


    }

    function makeImageTools(){
        imgSlider.querySelectorAll('.img-toolbar__tools a:not([href])').forEach(link => {
                let div = link.closest('div[id]');
                let i = Array.from(div.parentElement.children).indexOf(div);
                link.addEventListener('click', e => {
                    e.preventDefault();
                    if (link.classList.contains('img-tool-info')){
                        imgSlider.querySelectorAll('details > summary').forEach(s => s.click());
                    } else if (link.classList.contains('img-tool-zoom')){
                        gallery.view(i);
                    }
                })
            }
        )
    }

    function makeImageViewer(){

        const toolbarOpts = ['prev',  'zoomOut', 'zoomIn', 'reset', 'rotateLeft','rotateRight', 'next'];
        let imgCtr = document.querySelector('.image-slider');
        let images = imgCtr.querySelectorAll('a[data-img]');
        let toolbar = {};

        // First make the toolbar options
        toolbarOpts.forEach(opt => {
            let show = 1;
            // Remove next|prev if we don't need them
            if ((opt === 'next' || opt === 'prev') && images.length < 2){
                show = 0;
            }
            toolbar[opt] = {};
            toolbar[opt]['show'] = show;
            toolbar[opt]['size'] = 'large';
        });

        /*  We need to figure out some way to get the gallery transitions
            to work a bit better: we don't want the image loading in, but we
            do want it in all other cases.
        */
        let currTitle;
        gallery = new Viewer(imgCtr, {
            url: (img) => {
                return img.parentNode.getAttribute('data-img');
            },
            title: (img) => {
                //Set the current title for easy access later
                currTitle = img.alt;
                return currTitle;
            },
            transition: true,
            container: dmViewerContainer,
            ready: function(e){
                //Helpers
                let self = gallery;
                let title = self.title;
                let toolbarCtr = self.toolbar.querySelector('ul');
                let btns = toolbarCtr.querySelectorAll('li[role="button"]');
                toolbarCtr.addEventListener('mouseleave', e=>{
                    title.innerHTML = currTitle;
                });
                btns.forEach(btn => {
                    //Get caption
                    let pseudo = window.getComputedStyle(btn, ':before');
                    let caption = pseudo.content.replaceAll('"','');
                    btn.addEventListener('mouseenter', e =>{
                        title.classList.add('btn-caption')
                        title.innerHTML = caption;
                    });
                    btn.addEventListener('mouseleave', e => {
                        title.classList.remove('btn-caption');
                    });
                });
            },
            toolbar
        });

        images.forEach( a => {
            a.classList.add('zoomable');
            a.addEventListener('click', e => {
                e.preventDefault();
            })
        });
    }


    // Let's do some browse lazy loading...
    function enhanceLazyLoad(){
        let lazy = new LazyLoad();
        lazy.noImg = document.body.dataset.dmNoImg;
    }
})();