;(function (define) {
    'use strict';
    define(["underscore", "gettext", "backbone", "text!common/templates/components/paging-footer.underscore"],
        function(_, gettext, Backbone, paging_footer_template) {

            var PagingFooter = Backbone.View.extend({
                events : {
                    "click .next-page-link": "nextPage",
                    "click .previous-page-link": "previousPage",
                    "change .page-number-input": "changePage"
                },

                initialize: function(options) {
                    this.collection = options.collection;
                    this.hideWhenOnePage = options.hideWhenOnePage || false;
                    this.collection.bind('add', _.bind(this.render, this));
                    this.collection.bind('remove', _.bind(this.render, this));
                    this.collection.bind('reset', _.bind(this.render, this));
                    this.render();
                },

                render: function() {
                    var onFirstPage = !this.collection.hasPreviousPage(),
                        onLastPage = !this.collection.hasNextPage();
                    if (this.hideWhenOnePage) {
                        if (this.collection.totalPages <= 1) {
                            this.$el.addClass('hidden');
                        } else if (this.$el.hasClass('hidden')) {
                            this.$el.removeClass('hidden');
                        }
                    }
                    this.$el.html(_.template(paging_footer_template, {
                        current_page: this.collection.getPage(),
                        total_pages: this.collection.totalPages
                    }));
                    this.$(".previous-page-link").toggleClass("is-disabled", onFirstPage).attr('aria-disabled', onFirstPage);
                    this.$(".next-page-link").toggleClass("is-disabled", onLastPage).attr('aria-disabled', onLastPage);
                    return this;
                },

                changePage: function() {
                    var collection = this.collection,
                        currentPage = collection.getPage(),
                        pageInput = this.$("#page-number-input"),
                        pageNumber = parseInt(pageInput.val(), 10),
                        validInput = true;
                    if (!pageNumber || pageNumber > collection.totalPages || pageNumber < 1) {
                        validInput = false;
                    }
                    // If we still have a page number by this point,
                    // and it's not the current page, load it.
                    if (validInput && pageNumber !== currentPage) {
                        collection.setPage(pageNumber);
                    }
                    pageInput.val(''); // Clear the value as the label will show beneath it
                },

                nextPage: function() {
                    this.collection.nextPage();
                },

                previousPage: function() {
                    this.collection.previousPage();
                }
            });

            return PagingFooter;
        }); // end define();
}).call(this, define || RequireJS.define);
