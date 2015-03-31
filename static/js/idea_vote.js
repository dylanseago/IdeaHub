/**
 * Created by Dylan on 30/03/2015.
 */
$(document).ready(function() {
    // Idea vote event handler
    $("button.idea-vote-button").click(function () {
        var ideaVoteWrapper = $(this).closest(".idea-vote-wrapper");
        var ideaId = ideaVoteWrapper.data('idea-id');
        var likes = ideaVoteWrapper.data('idea-likes');
        var dislikes = ideaVoteWrapper.data('idea-dislikes');
        var isLike = $(this).hasClass('idea-vote-button-like');
        var rating = isLike ? 1 : -1;
        if (!$(this).hasClass('active')) {
            // User added their rating
            $(this).addClass('active');
            var otherButton = $(this).siblings('button.idea-vote-button');
            // Remove previous rating
            if (otherButton.hasClass('active')) {
                otherButton.removeClass('active');
                if (isLike) {
                    dislikes -= 1;
                } else {
                    likes -= 1;
                }
            }
            if (isLike) {
                likes += 1;
            } else {
                dislikes += 1;
            }
        } else {
            // User removed their rating
            $(this).removeClass('active')
            rating = 0;
            if (isLike) {
                likes -= 1;
            } else {
                dislikes -= 1;
            }
        }
        var likePercent, dislikePercent;
        if (likes + dislikes == 0) {
            likePercent = 0;
            dislikePercent = 0;
        } else {
            likePercent = (likes / (likes + dislikes)) * 100;
            dislikePercent = dislikes == 0 ? 0 : 100 - likePercent;
        }
        ideaVoteWrapper.data('idea-likes', likes);
        ideaVoteWrapper.data('idea-dislikes', dislikes);
        ideaVoteWrapper.find('.idea-likes').text(likes);
        ideaVoteWrapper.find('.idea-dislikes').text(dislikes);
        ideaVoteWrapper.find('.idea-likes-percent').css('width', likePercent + '%');
        ideaVoteWrapper.find('.idea-dislikes-percent').css('width', dislikePercent + '%');
        // Perform ajax call to rate the idea
        $.post('/idea/' + ideaId + '/rate', {
            rating: rating
        }).done(function() {
            console.log("Successfully rated idea " + ideaId);
        }).fail(function() {
            console.log("Failed to rate idea " + ideaId);
        });
    });
});