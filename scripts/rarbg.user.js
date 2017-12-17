// ==UserScript==
// @id rarbg-thumbnailer@petervaro
// @name Add thumbnails to list of torrents
// @namespace petervaro
// @include https://rarbg.to/torrents.php*
// @author Peter Varo
// @version 0.0.9
// @updateURL https://gist.github.com/petervaro/e724393ec00b9934915c/raw/dd6eb6b5a4a95ff55db1128a1c53c98dd4e7715f/rarbg.user.js
// @grant none
// ==/UserScript==
(function ()
{
    'use strict';

    /* Constants */
    var IMG_PATTERN = /<img\s+src\s*=\s*(\\?('|"))\s*(.+?)\s*(\\?('|")).*?>/gi.source;

    /* Variables */
    var i,
        a,
        img,
        source,
        category,
        torrent,
        torrents = document.getElementsByClassName('lista2');

    /* For each torrent in the list */
    for (i=0; i<torrents.length; i++)
    {
        /* If torrent does not have a category */
        if (!(category = torrents[i].childNodes[0]))
            continue;

        /* If torrent category is porn */
        if (category.childNodes[0].getAttribute('href') === '/torrents.php?category=4')
            continue;

        /* If torrent does not have a link */
        if (!(torrent = torrents[i].childNodes[1]))
            continue;

        /* If link does not provide a mouse-over image */
        a = torrent.childNodes[0];
        if (!(source = (new RegExp(IMG_PATTERN, 'gi')).exec(a.getAttribute('onmouseover'))))
            continue;

        /* Remove mouse-over action */
        a.setAttribute('onmouseover', undefined);

        /* Create new image object based on the mouse-over action */
        img     = document.createElement('img');
        img.src = source[3];
        img.style.float = 'left';
        img.style.marginRight = '10px';

        /* Render image to the DOM */
        torrent.insertBefore(img, a);
    }
})();
